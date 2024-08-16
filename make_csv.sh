#!/bin/bash

# Set Environment Variables

export XML_FILE="./KindleSyncMetadataCache.xml"
export OUTPUT_CSV="./output.csv"


# Write CSV Headers
echo "ASIN,Title,Author,Publisher,Publication Date,Purchase Date" > "$OUTPUT_CSV"

# Parse XML and extract attributes then add row
xmlstarlet sel -T -t \
    -m "//meta_data" \
    -v "ASIN" -o "," \
    -v "concat('\"', normalize-space(title), '\"')" -o "," \
    -v "concat('\"', normalize-space(authors/author), '\"')" -o "," \
    -v "concat('\"', normalize-space(publishers/publisher), '\"')" -o "," \
    -v "publication_date" -o "," \
    -v "purchase_date" -n \
    "$XML_FILE" >> "$OUTPUT_CSV"
