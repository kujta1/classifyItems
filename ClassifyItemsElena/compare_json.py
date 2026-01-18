

import json

# Load the JSON data from both files
with open('ista_klasa_items_old.json', 'r', encoding='utf-8') as file1, \
     open('ista_klasa_items.json', 'r', encoding='utf-8') as file2:
    products_old = json.load(file1)
    products_new = json.load(file2)

# Extract product IDs or relevant identifiers into sets
ids_old = {product["_id"] for product in products_old}
ids_new = {product["_id"] for product in products_new}

# Find unique products
unique_to_old = ids_old - ids_new  # Products in the old file not in the new file
unique_to_new = ids_new - ids_old  # Products in the new file not in the old file

# Prepare the results
results = {
    "unique_to_ista_klasa_items_old": [],
    "unique_to_ista_klasa_items_new": []
}

# Populate the unique products
for product in products_old:
    if product["_id"] in unique_to_old:
        results["unique_to_ista_klasa_items_old"].append(product)

for product in products_new:
    if product["_id"] in unique_to_new:
        results["unique_to_ista_klasa_items_new"].append(product)

# Write the results to a new JSON file
with open('unique_products.json', 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)

print("Unique products have been saved to unique_products.json")