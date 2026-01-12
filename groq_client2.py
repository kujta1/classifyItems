import json
import re
import json
from groq import Groq

MODEL = "llama-3.3-70b-versatile"
client = Groq()

# PROMPT_TEMPLATE = """
# Ти си експерт за извлекување и структурирање на податоци за производи.
#
# ЦЕЛ:
# Од дадениот опис на производ (на македонски јазик), извлечи структурирани податоци и карактеристики.
#
# СТРОГИ ПРАВИЛА:
# - Излезот МОРА да биде валиден JSON.
# - СИТЕ клучеви и вредности МОРА да бидат на македонски јазик.
# - Не измислувај податоци.
# - Ако недостасува вредност, постави null.
# - Не додавај дополнителен текст.
#
# JSON СТРУКТУРА:
# {
#   "тип_на_производ": string,
#   "боја": string,
#   "компоненти": [
#     {
#       "тип_на_компонента": string,
#       "материјал": string | null,
#       "тип_на_греење": string | null,
#       "број_на_грејни_места": number | null,
#       "контроли": string | null,
#       "функции": [string],
#       "капацитет_литри": number | null,
#       "енергетска_класа": string | null,
#       "начин_на_чистење": string | null,
#       "димензии_мм": {
#         "ширина": number | null,
#         "висина": number | null,
#         "длабочина": number | null
#       }
#     }
#   ]
# }
#
# ВЛЕЗ:
# {description}
# """


PROMPT_TEMPLATE = """
You are a strict information extraction engine for kitchen appliances.

TASK:
Using ONLY the content of FormattedDescription:
1. Identify the product type from SHP_CATEGORIES
2. Extract ALL explicitly mentioned characteristics
3. Output ONLY valid JSON matching EXACTLY the schema below

IMPORTANT RULES:
- Use ONLY FormattedDescription
- Do NOT infer or guess
- If information is missing → use null
- Do NOT add fields
- Do NOT explain
- Output ONLY JSON
- Language MUST be Macedonian

--------------------------------
SHP_CATEGORIES (EXACT VALUES)
--------------------------------
- Вградливи сетови од рерна и плотна
- Вградливи фурни и плотни
- Вградливи рерни
- Вградливи плотни
- Микробранови печки
- Шпорети

--------------------------------
JSON SCHEMA (STRICT)
--------------------------------
{
  "тип_на_производ": string,
  "боја": string | null,
  "компоненти": [
    {
      "тип_на_компонента": string,
      "материјал": string | null,
      "тип_на_греење": string | null,
      "број_на_грејни_места": number | null,
      "контроли": string | null,
      "функции": [string],
      "капацитет_литри": number | null,
      "енергетска_класа": string | null,
      "начин_на_чистење": string | null,
      "димензии_мм": {
        "ширина": number | null,
        "висина": number | null,
        "длабочина": number | null
      }
    }
  ]
}

--------------------------------
FEW-SHOT EXAMPLES
--------------------------------

FormattedDescription:
"Вградна рерна и стаклокерамичка плотна во сет. Плотна со 4 зони и TouchControl. Рерна 77L, енергетска класа A, AquaClean. Димензии 595x595x564 мм."

Output:
{
  "тип_на_производ": "Вградливи сетови од рерна и плотна",
  "боја": null,
  "компоненти": [
    {
      "тип_на_компонента": "Плотна",
      "материјал": "Стаклокерамика",
      "тип_на_греење": "Електрично",
      "број_на_грејни_места": 4,
      "контроли": "TouchControl",
      "функции": [],
      "капацитет_литри": null,
      "енергетска_класа": null,
      "начин_на_чистење": null,
      "димензии_мм": {
        "ширина": null,
        "висина": null,
        "длабочина": null
      }
    },
    {
      "тип_на_компонента": "Рерна",
      "материјал": null,
      "тип_на_греење": null,
      "број_на_грејни_места": null,
      "контроли": null,
      "функции": [],
      "капацитет_литри": 77,
      "енергетска_класа": "A",
      "начин_на_чистење": "AquaClean",
      "димензии_мм": {
        "ширина": 595,
        "висина": 595,
        "длабочина": 564
      }
    }
  ]
}

--------------------------------
NOW PROCESS THIS INPUT

FormattedDescription:
{description}
"""



def filter_products_by_breadcrumbs(
    input_file: str,
    output_file: str
):
    TARGET_CATEGORIES = [
        "Вградливи сетови од рерна и плотна",
        "Вградливи фурни и плотни",
        "Вградливи рерни",
        "Вградливи плотни",
        "Микробранови печки",
        "Шпорети"
    ]

    # Load products
    with open(input_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    filtered_products = []

    for item in products:
        breadcrumbs = item.get("Breadcrumbs", "")

        for category in TARGET_CATEGORIES:
            if re.search(category, breadcrumbs, re.IGNORECASE):
                filtered_products.append(item)
                break  # avoid duplicates

    # Write filtered products
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_products, f, ensure_ascii=False, indent=4)

    return filtered_products

filtered = filter_products_by_breadcrumbs(
    input_file="products.json",
    output_file="filtered_products.json"
)



def enrich_filtered_products(input_file: str, output_file: str) -> list[dict]:
    """
    Reads a filtered products JSON file, extracts structured data for each product using Groq,
    enriches each product with 'structuredData', prints it in terminal, and saves the enriched JSON.

    Returns the list of enriched products.
    """
    # Load filtered products
    with open(input_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        description = product.get("FormattedDescription") or product.get("Description") or ""
        if not description:
            continue

        # Groq API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": PROMPT_TEMPLATE.replace("{description}", description)}
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON safely
        try:
            structured = json.loads(content)
        except json.JSONDecodeError:
            print("❌ JSON parse error:")
            print(content)
            structured = None

        product["structuredData"] = structured

        # Print structured data to terminal
        if structured:
            print(json.dumps(structured, ensure_ascii=False, indent=2))

    # Save enriched products
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"✅ Processing completed: saved to {output_file}")
    return products




print(len(filtered))
enriched_products = enrich_filtered_products(
    input_file="filtered_products.json",
    output_file="filtered_products_enriched.json"
)
