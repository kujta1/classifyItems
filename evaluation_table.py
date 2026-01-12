import json

# Shporeti categories
SHP_CATEGORIES = [
    "Вградливи сетови од рерна и плотна",
    "Вградливи фурни и плотни",
    "Вградливи рерни",
    "Вградливи плотни",
    "Микробранови печки",
    "Шпорети"
]

# Include 'other' for anything outside Shporeti
ALL_CATEGORIES = SHP_CATEGORIES + ["other"]

# Load mismatched items
with open("razlichni_klasi_items.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# Initialize evaluation table
eval_table = {cat: {"new": 0, "old": 0} for cat in ALL_CATEGORIES}

# Fill evaluation table
for item in items:
    result = item.get("result", "").lower()  # 'new' or 'old'
    old = item.get("category_previously_human_readable", "").strip()
    new = item.get("category_predicted_human_readable", "").strip()

    # Map anything outside SHP_CATEGORIES to 'other'
    if old not in SHP_CATEGORIES:
        old = "other"
    if new not in SHP_CATEGORIES:
        new = "other"

    # Count as new/old better
    if result == "new":
        eval_table[new]["new"] += 1
    elif result == "old":
        eval_table[old]["old"] += 1

# Print nicely formatted table
print(f"{'Category':40} | {'New better':10} | {'Old better':10}")
print("-" * 70)
for cat in ALL_CATEGORIES:
    print(f"{cat:40} | {eval_table[cat]['new']:10} | {eval_table[cat]['old']:10}")
