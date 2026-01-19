import json
import time
import os
from groq import Groq

# Initialize Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def generate_structure(product_name, description_name):
    """
    Sends product info to Groq and returns a short, cleaned-up summary.
    """
    prompt = f"""
Ти си експерт за извлекување и структурирање на податоци за производи.
Твојата задача е да направиш краток, јасен и професионален опис (Normalized Summary) на производот.

ПРАВИЛА:
1. Користи македонски јазик.
2. Биди концизен (максимум 2-3 реченици).
3. Наведи ги клучните карактеристики (димензии, капацитет, енергетска класа).
4. Не користи непотребни зборови како "Овој производ е..." или "Опис:".
5. Резултатот треба да биде само текстот за описот, без JSON структури.


ВЛЕЗНИ ПОДАТОЦИ:
Име: {product_name}
Опис: {description_name}

JSON СТРУКТУРА:
{{
'Бренд': 'име на бренд',
'Класа': 'енергетска класа',
'Вид на Ладење': 'NoFrost или конвенционално',
'Технологија': 'која технологија ја користи',
'Електронско Регулирање': true,
'Капацитет на ладење': 0,
'Капацитет на мрзнење': 0,
'Димензии': [0, 0, 0],
'LED': true,
'MultiAirflow систем': true,
'VitaFresh фиоки': true,
'Ниво на Бучава': 0,
'Краток_Опис': 'Краток и професионален опис на македонски (2-3 реченици)'
}}
# ПРАВИЛА ЗА КЛУЧЕВИТЕ:
# - "Бренд": Името на брендот.
# - "Класа": Енергетска класа (A++, A+, F, итн).
# - "Вид на Ладење": "NoFrost", има или не но фрост,
# - "Технологија": "Inteligent Inverter Technology", која технологија ја користи.
# - "Електронско Регулирање": true ако има , false ако нема.
# - "Капацитет на ладење": Капацитет на фрижидерот во литри (само број).
# - "Капацитет на мрзнење": Капацитет на замрзнувачот во литри (само број, 0 ако нема).
# - "Димензии": Листа од броеви [висина, ширина, длабочина] во цм.
# - "LED": true ако има LED осветлување, false ако нема.
# - "MultiAirflow систем": true ако има, false ако нема.
# - "VitaFresh фиоки": true ако има, false ако нема.
# - "Ниво на бучава": изразена во dB.
# РЕЗУЛТАТ: Врати исклучиво чист JSON објект.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            # max_tokens=150
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Грешка при повикување на Groq: {e}")
        return None

# Правил филтер на фрижидери и замрзнувачи и ги запишува во јсон
def process_products(input_file, output_file):
    # Ги вчитува продуктите
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

   # 2. Филтер на фрижидери и замрзнувачи
    target_keywords = ["фрижидер", "замрзнувач", "ладилници", "замрзнувачи", "ладилник"]
    filtered_products = []
    for p in products:
        text_to_check = (p.get("ProductName", "") + " " + p.get("Breadcrumbs", "")).lower()
        if any(keyword in text_to_check for keyword in target_keywords):
            filtered_products.append(p)

    print(f"Пронајдени {len(filtered_products)} производи за обработка.")

    # 3. The for Loop
    for i, product in enumerate(filtered_products):
        print(f"Процесирам {i + 1}/{len(filtered_products)}: {product.get('ProductName')}")

        # CALL THE AI (Now inside the loop)
        new_desc = generate_structure(
            product.get("ProductName", ""),
            product.get("Description", "")
        )

        # Апдејт на продукт дата
        if new_desc:
            # product["FormattedDescription"] = new_desc
            try:
                # Го претвораме стрингот во вистински JSON објект
                product["properties"] = json.loads(new_desc)
            except:
                product["properties"] = new_desc  # Fallback ако не е валиден JSON

        # PRINT THE GENERATED CONTENT
        print(f"ГЕНЕРИРАН ОПИС: {new_desc}")
        print("-" * 40)

        # Wait to respect Rate Limits
        time.sleep(2)

        # Save progress every 10 items
        if i % 10 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filtered_products, f, ensure_ascii=False, indent=4)

    # 4. Final save (Outside the loop - aligned with 'for')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_products, f, ensure_ascii=False, indent=4)

    print("Завршено! Сите производи се обработени и зачувани.")

if __name__ == "__main__":
    process_products('products.json', 'products_updated.json')

