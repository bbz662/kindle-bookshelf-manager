# Kindle Metadata to CSV Converter

This repository contains a shell script that converts metadata from a Kindle XML file (`KindleSyncMetadataCache.xml`) into a CSV file (`output.csv`). The script uses `xmlstarlet` to parse the XML and extract specific attributes like ASIN, Title, Author, Publisher, Publication Date, and Purchase Date.

## Locating the `KindleSyncMetadataCache.xml` File

The `KindleSyncMetadataCache.xml` file contains metadata for Kindle books and is typically found in different locations depending on your operating system. Below are the common locations for this file on various operating systems:

### Windows

On Windows, the `KindleSyncMetadataCache.xml` file is usually located in the following directory:

```plaintext
C:\Users\<YourUsername>\AppData\Local\Amazon\Kindle\Cache\KindleSyncMetadataCache.xml
```

To navigate to this directory:

1. Open `File Explorer`.
2. Enter `%LOCALAPPDATA%\Amazon\Kindle\Cache` in the address bar and press Enter.
3. Look for the `KindleSyncMetadataCache.xml` file in this directory.

### macOS

On macOS, the file can typically be found in the following location:

```plaintext
/Users/<YourUsername>/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml
```

To locate the file:

1. Open `Finder`.
2. In the menu bar, select `Go` > `Go to Folder...`.
3. Enter the following path: `~/Library/Application Support/Kindle/Cache/`
4. Look for the `KindleSyncMetadataCache.xml` file in this directory.

### Linux (with Kindle installed via Wine)

If you are running Kindle via Wine on Linux, the file may be located in a directory similar to:

```plaintext
~/.wine/drive_c/users/<YourUsername>/Local Settings/Application Data/Amazon/Kindle/Cache/KindleSyncMetadataCache.xml
```

To find the file:

1. Open a terminal.
2. Navigate to the directory with the command:
   ```bash
   cd ~/.wine/drive_c/users/<YourUsername>/Local\ Settings/Application\ Data/Amazon/Kindle/Cache/
   ```
3. Use the `ls` command to list the files and locate `KindleSyncMetadataCache.xml`.

### Verifying the File Location

If you're unsure where the file is located, you can use the search functionality of your OS:

- **Windows**: Use the search bar in the Start Menu or File Explorer to search for `KindleSyncMetadataCache.xml`.
- **macOS**: Use Spotlight Search (Cmd + Space) and enter `KindleSyncMetadataCache.xml`.
- **Linux**: Use the `find` command in the terminal:
  ```bash
  find ~ -name "KindleSyncMetadataCache.xml"
  ```

Once you locate the file, ensure that the `XML_FILE` environment variable in the script points to this location.

## Prerequisites

Ensure the following tools are installed on your system:

- **bash**: The script is written for Bash and should work on any Unix-like system.
- **xmlstarlet**: A command-line XML processor that is used to parse and extract data from the XML file.
- **Python**: 3.x
- **requests**: A library to make HTTP requests.
- **python-dotenv**: A library to load environment variables from a .env file.

### Installation of `xmlstarlet`

For **Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install xmlstarlet
```

For **CentOS/Fedora**:
```bash
sudo yum install xmlstarlet
```

For **macOS** (using Homebrew):
```bash
brew install xmlstarlet
```

```bash
pip install requests python-dotenv
```

## Usage

1. **Place the XML File:**

   Ensure that the `KindleSyncMetadataCache.xml` file is located in the same directory as the script, or modify the `XML_FILE` variable in the script to point to the correct location.

2. **Run the Script:**

   Execute the script using Bash:

   ```bash
   ./make_csv.sh
   ```

   ```bash
   python ./add_category.py

   ```

3. **Check the Output:**

   After running the script, the output CSV file (`output.csv`, `output_with_category.csv`) will be generated in the same directory.

## Script Details

### Environment Variables

- `XML_FILE`: Specifies the path to the XML file to be parsed.
- `OUTPUT_CSV`: Specifies the path to the output CSV file.

### CSV Headers

The script initializes the CSV file with the following headers:
- `ASIN`
- `Title`
- `Author`
- `Publisher`
- `Publication Date`
- `Purchase Date`

### XML Parsing and Data Extraction

The script uses `xmlstarlet` to:

- Select each `<meta_data>` element in the XML.
- Extract values from the `ASIN`, `title`, `author`, `publisher`, `publication_date`, and `purchase_date` elements.
- Write the extracted data into the CSV file.

## Customization

You can customize the script by modifying the XPath expressions or adding additional fields to extract more data from the XML.
