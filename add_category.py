import asyncio
import csv
import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def get_env_var(var_name, default_value=None, required=False):
    value = os.getenv(var_name, default_value)
    if required and value is None:
        raise ValueError(f"Environment variable {var_name} is missing and is required.")
    return value

INPUT_CSV = get_env_var('INPUT_CSV', required=True)
OUTPUT_CSV = get_env_var('OUTPUT_CSV', required=True)
GEMINI_MODEL = get_env_var('GEMINI_MODEL', required=True)
GEMINI_API_KEY = get_env_var('GEMINI_API_KEY', required=True)
DEFAULT_OUTPUT_MAX_TOKENS = 100
OUTPUT_MAX_TOKENS = int(get_env_var('OUTPUT_MAX_TOKENS', DEFAULT_OUTPUT_MAX_TOKENS))
RATE_LIMIT_MS = int(get_env_var('RATE_LIMIT_MS', 300))

PROMPT_TEMPLATE = """Based on the information provided (ASIN, Title, Author, Publisher, Publication Date, Purchase Date), infer the genre of the book or manga. 
Select few genres from the following list commonly used in the Kindle Store:

**Possible Genres:**
- Literature & Fiction
- Mystery, Thriller & Suspense
- Science Fiction & Fantasy
- Romance
- Historical Fiction
- Horror
- Biographies & Memoirs
- Self-Help
- Children's eBooks
- Teen & Young Adult
- Comics & Graphic Novels
- Manga
- Business & Money
- Health, Fitness & Dieting
- Religion & Spirituality
- Cookbooks, Food & Wine
- History
- LGBTQ+ eBooks
- Politics & Social Sciences
- Parenting & Relationships
- Travel
- Arts & Photography
"""

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "Categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"}
                },
                "required": ["category"],
                "additionalProperties": False
            }
        }
    },
    "required": ["Categories"],
    "additionalProperties": False
}

async def get_gemini_response(prompt, model, api_key, max_output_tokens, json_schema=None):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        if json_schema:
            prompt += f"\nUse the following JSON schema for your response:\n{json.dumps(json_schema, indent=2)}"

        headers = {'Content-Type': 'application/json'}
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_output_tokens,
                "responseMimeType": "application/json" if json_schema else "text/plain"
            }
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
        except ValueError as e:
            print("Failed to Gemini Request:", e)
            print("Response content:", response.text)
            return "Error"
        
        try:
            data = response.json()
        except ValueError as e:
            print("Failed to parse JSON:", e)
            print("Response content:", response.text)
            return "Error"

        if not response.ok:
            print(f"Error: {response.status_code}")
            raise ValueError(f"{response.status_code} {json.dumps(data, indent=2)}")
        try:
            categories = json.loads(data['candidates'][0]['content']['parts'][0]['text'])
            category_list = [item['category'] for item in categories['Categories']]
            return ", ".join(category_list)
        except ValueError as e:
            print("Failed to load JSON:", e)
            print("Response content:", data['candidates'][0]['content']['parts'][0]['text'])
            return "Error"

    except Exception as error:
        print(f"Error in get_gemini_response ({model}): {error}")
        return "Error"

async def process_csv(input_csv, output_csv, prompt_template, model, api_key, max_output_tokens, json_schema, rate_limit_ms):
    tasks = []

    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Category']
        rows = list(reader)

    for row in rows:
        prompt = prompt_template.format(
            ASIN=row['ASIN'], 
            Title=row['Title'], 
            Author=row['Author'], 
            Publisher=row['Publisher'], 
            PublicationDate=row['Publication Date'], 
            PurchaseDate=row['Purchase Date']
        )
        tasks.append(get_gemini_response(prompt, model, api_key, max_output_tokens, json_schema))
        await asyncio.sleep(rate_limit_ms / 1000.0)

    categories = await asyncio.gather(*tasks)

    for row, category in zip(rows, categories):
        row['Category'] = category

    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file with category added is saved as '{output_csv}'.")

if __name__ == "__main__":
    print("Script start")
    asyncio.run(process_csv(INPUT_CSV, OUTPUT_CSV, PROMPT_TEMPLATE, GEMINI_MODEL, GEMINI_API_KEY, OUTPUT_MAX_TOKENS, JSON_SCHEMA, RATE_LIMIT_MS))
    print("Script end")
