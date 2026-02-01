import json

SHP_CATEGORIES = [
    "Аспиратори",
    "Бојлери"
]


# Include 'other' for anything outside Shporeti
ALL_CATEGORIES = SHP_CATEGORIES + ["other"]

# Load mismatched items
with open("razlichni_klasi_items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# Initialize confusion matrix
conf_matrix = {old: {new: 0 for new in ALL_CATEGORIES} for old in ALL_CATEGORIES}

# Fill confusion matrix
for item in items:
    old = item.get("category_previously_human_readable", "").strip()
    new = item.get("category_predicted_human_readable", "").strip()

    # Map anything outside SHP_CATEGORIES to 'other'
    if old not in SHP_CATEGORIES:
        old = "other"
    if new not in SHP_CATEGORIES:
        new = "other"

    conf_matrix[old][new] += 1

# Print nicely formatted confusion matrix
# Header
header = ["Old \\ New"] + ALL_CATEGORIES
print("\t".join(f"{h:25}" for h in header))
print("-" * 25 * (len(ALL_CATEGORIES)+1))

# Rows
for old in ALL_CATEGORIES:
    row = [old] + [str(conf_matrix[old][new]) for new in ALL_CATEGORIES]
    print("\t".join(f"{cell:25}" for cell in row))