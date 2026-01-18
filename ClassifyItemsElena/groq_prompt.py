import json
import time
from groq import Groq


API_KEY = ' your_groq_api_key_here '  # Replace with your actual Groq API key
client = Groq(api_key=API_KEY)

def get_formatted_description(product_name, description):
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
Опис: {description}

JSON СТРУКТУРА:
{{
"тип": "Аспиратор",
"марка": "име на бренд",
"тежина кг": број во кг,
"моќност W": врој во W,
"капацитет л": број во литри,
"ниво на бучава dB": број во dB,            
"материјал": " инокс",                       
"изолација": " број во см",                                                                    
"максимална температура": број во °C,                                                         
"функции": ["Турбо режим", "LED осветлување"],                                                                                              
"монтажа": "Внатрешна",                      
"боја": "Сива",                           
"контроли": "Термостат",                                                                     
"вшмукувачка моќ m³/h": број во m³/h,                                   
"осветлување": "LED",                                   
"дијаметар на одводно црево см": број во см,                      
"филтери": "HEPA",                                        
"димензија": [ширина, висина, длабочина] во мм            
}}

# ПРАВИЛА ЗА КЛУЧЕВИТЕ:
# - "Marka": Името на брендот.
# - "class": Енергетска класа (A++, A+, F, итн).
# - "tip_ladenje": "NoFrost", има или не но фрост,
# - "tehnologija": "Inteligent Inverter Technology", која технологија ја користи.
# - "електронско регулирање": true ако има , false ако нема.
# - "Kapacitet_ladenje": Капацитет на фрижидерот во литри (само број).
# - "kapacitet_mrznenje": Капацитет на замрзнувачот во литри (само број, 0 ако нема).
# - "dimenzija": Листа од броеви [висина, ширина, длабочина] во цм.
# - "LED": true ако има LED осветлување, false ако нема.
# - "MultiAirflow систем": true ако има, false ако нема.
# - "VitaFresh фиоки": true ако има, false ако нема.
# - "Ниво на бучава": изразена во dB.
# - "тип": "Име на типот на производ (Аспиратор или Бојлер)",
# - "марка": "името на бренд",
# - "тежина кг": тежина на производот во кг,
# - "моќност W": моќност во W,
# - "капацитет л": капацитет во литри,
# - "ниво на бучава dB": ниво на бучава во dB,            
# - "материјал": " инокс",                       
# - "изолација": " видот на изолација и димензијата на истата во см",                                                                    
# - "максимална температура": број во °C,                                                         
# - "функции": ["Турбо режим", "LED осветлување"],                                                                                              
# - "монтажа": "Начин на монтажа (Внатрешна, Надворешна, високо монтажна, итн)",                      
# - "боја": "боја на производот (Сива, Бела, Црна, итн)",                           
# - "контроли": "начин на контроли (Термостат, Електронски, итн)",                                                                     
# - "вшмукувачка моќ m³/h": моќност на вшмукување во m³/h,                                   
# - "осветлување": "начин на осветлување (LED, Халогенско, итн)",                                   
# - "дијаметар на одводно црево см": ширина на цревото (дијаметар) во см,                      
# - "филтери": "HEPA",                                        
# - "димензија": [ширина, висина, длабочина] во мм  
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


def process_products(input_file, output_file):
    # Ги вчитува продуктите
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    target_keywords = ["аспиратор", "бојлер", "проточен", "проточна", "ладилник"]
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
        new_desc = get_formatted_description(
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