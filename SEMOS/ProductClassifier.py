#from openai import OpenAI
import json
from conf_file import openAi_key, groq_api
from groq import Groq

product_json = {
        "ProductName" : "Bosch WNG254A0BY",
        "Description" : "» › › » WNG254A0BY\nWNG254A0BY\nOпис:\nWNG254A0BY e seria 6, A класа Пере-Суши\nКапацитет: 10кг. пере/ 6кг. суши\nКонтинуирано перење и сушење за 6 кг. веш\nКапацитет 1-10 кг.\nВртежи 1400\nXXL волумен на барабанот: 65 л.\nЕнергетска ефикасност:  А класа\nVarioPerfect: заштеда на време или енергија\nAutoDry: нежно сушење на алиштата до саканото ниво на сувост со помош на интелегентните сензори\nSuperQuick 15′: брза програма која овозможува да се измијат 2кг алишта за рекордно време од 15 минути\nОсвежувач: Да\nПрилагодлива температура на сушење: Да\nПриказ на предозирање: Да\nКонтрола на пената: Да\nПрограми:\nПред Перење, Екстра плакнење, Центрифуга, Кошули/Блузи, Спорт/Фитнес’, Памук, Темно Перење, Алергија Плус, Lingerie, Волна-рачно перење..\nПрограми преку апликацијата: Алергија плус, јоргани, крпи, кошули / блузи\nАвтоматско сушење, Временски програми\nAntiStain: детектира и отстранува 4 најчести дамки, без помош на хемикалии\nМожност за ладно перење без температура\nДодатни функции:\nVarioPerfect: заштеда на време или енергија\nIron Assist: дополнителниот третман со пареа ја намалува или дури целосно ја елиминира потребата за пеглање на суви алишта\nVarioPerfect: заштеда на време или енергија\nWash & Dry 60: ефикасно перење и сушење за мала количина на алишта за само 60 мин.\nАвтоматско сушење, Временски програми\nReload function: функција која Ви овозможува да додадете алишта по веќе започнато перење\nКомфорт/Сигурност:\nVarioDrum: специјален бубањ за тивко и нежно перење на алиштата\nШирока врата од 32 см, бела/црно-сива боја и агол на отворање 130 °\nAntiVibration Design: за потивка и постабилна машина\nКонтрола за нерамнотежата на бубањот\nЗвучна изолација преку долниот капак\nActiveWaterPlus: еколошко зачувување водата и животната средина и заштеда на пари\nИндикатор за потрошувачка: информации за потрошувачката на енергија и вода\nОсветлено копче за избор на програма со интегрирано копче за вклучување / исклучување\nLED Голем екран: Ви прикажува информации за перењето со преостанато време и препорачување на полнење на бубањот со индикатор за потрошувачка\nTimer: можност за одложен старт 1-24 часа\nИзбирање на звучен сигнал\nСамоочистувачка преграда за средства за чистење\nТехнички информации:\nНиво на бучавост при стандардна програма памук 60° C: 47 dB\nЗаклучување на пералната како опција за деца\nМожност за вградување под работна површина\nДимензии : (В x Ш x Д): 84.8 x 59.8 x 59 см\nЕнергетска класа од 2022г. E\n  \ne mail: ",
        "ProductUrl" : "https://vudelgo.com.mk/wng254a0by/",
        "StoreName" : "vudelgo",
        "ProductImg" : "https://vudelgo.com.mk/wp-content/uploads/2018/02/WNG254U0BY-14.jpg",
        "Breadcrumbs" : "Vudelgo-Bosch-Пере и Суши 2 in 1-Перење и сушење на алишта-",
        "FormattedDescription" : "'Bosch WNG254A0BY, Серија 6, класа A Перење/Сушење. Капацитет: 10кг перење/6кг сушење. 1400 вртежи, XXL барабан 65л. VarioPerfect, AutoDry, SuperQuick 15', AntiStain. Програми: Пред перење, Памук, Алергија Плус. Дополнителни функции: Iron Assist, Wash&Dry 60. VarioDrum, AntiVibration Design, ActiveWater Plus. Димензии: 84.8 x 59.8 x 59 см.'",
        "_id" : "669a8f36655d7ec447bad6d0",
        "Category" : "67f71a03523d00258894a4dc"
    }
category_json = {
        "_id" : "67f71a03523d00258894a4dc",
        "name" : "Машини за перење и сушење алишта",
        "description" : "Combined washer-dryer machines designed for both laundry washing and drying in a single unit.",
        "parent_id" : "67f71a03523d00258894a4d9",
        "hasChilds" : "false",
        "tags" : [

        ]
    }
class ProductClassifier:
    def __init__(self, category_json: dict, product_json: dict, api_key: str):
        self.category = category_json
        self.product = product_json
        #self.client = OpenAI(api_key=api_key)
        self.client = Groq(api_key=api_key)

    def is_match(self) -> bool:
        category_text = json.dumps(self.category, ensure_ascii=False, indent=2)
        product_text = json.dumps(self.product, ensure_ascii=False, indent=2)

        # response = self.client.chat.completions(
        #     model="gpt-4.1-mini",
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            # input=[
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a strict product-category classifier.\n"
                        "Return ONLY 'true' or 'false'.\n"
                        "No explanations."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Category JSON:\n{category_text}\n\n"
                        f"Product JSON:\n{product_text}\n\n"
                        "Question:\n"
                        "Does the product belong to this category?"
                    )
                }
            ],
            temperature=0,
        )

        # answer = response.output_text.strip().lower()
        answer = response.choices[0].message.content.strip().lower()
        return answer == "true"

if __name__ == "__main__":
    matcher = ProductClassifier(
        category_json=category_json,
        product_json=product_json,
        api_key=openAi_key
    )

    print(matcher.is_match())
