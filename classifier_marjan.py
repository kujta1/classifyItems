import re
from classifier import Classifier
from evaluate import Evaluation


class ClassifierFrizideri(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4d7",
                                     "67f71a03523d00258894a4d8",
                                     ], classes_map={
        "67f71a03523d00258894a4d7": "Фрижидери",
        "67f71a03523d00258894a4d8": "Замрзнувачи",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        # TODO
        # Vashiot KOD TUKA
        breadcrumbs = item.get("Breadcrumbs", "")
        product_name = item.get("ProductName", "").lower()

        # Classifying as 'Фрижидери'
        if (re.search("фрижидер", breadcrumbs, re.IGNORECASE) or
            re.search("фрижидер", product_name, re.IGNORECASE) or
            re.search("ладилници", breadcrumbs, re.IGNORECASE) or
            re.search("ладилник", product_name, re.IGNORECASE)) and \
                not re.search("дополнителна опрема", breadcrumbs, re.IGNORECASE) and \
                not re.search("магнети", breadcrumbs, re.IGNORECASE) and \
                not re.search("Преносни фрижидери", breadcrumbs, re.IGNORECASE) and \
                not re.search("Акумулаторски фрижидер", product_name, re.IGNORECASE) and \
                not re.search("шпорет", product_name, re.IGNORECASE):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]

        # Classifying as 'Замрзнувачи'
        elif re.search("замрзнувач", breadcrumbs, re.IGNORECASE) or re.search("замрзнувач", product_name,
                                                                              re.IGNORECASE):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]

        else:
            return None, None

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA
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
    Име: {item["ProductName"]}
    Опис: {item["Description"]}

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

        pass

evaluator = Evaluation(ClassifierFrizideri())

evaluator.evaluate_All_products()
