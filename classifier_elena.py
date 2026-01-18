import re
from classifier import Classifier
from evaluate import Evaluation

class ClassifierOstanato(Classifier):
    def __init__(self, classes_list=["67f71a03523d00258894a4e4",
                                     "67f71a03523d00258894a4e5",
                                     ], classes_map={
        "67f71a03523d00258894a4e4": "Аспиратори",
        "67f71a03523d00258894a4e5": "Бојлери",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)
    
    def classify(self, item):
        breadcrumbs = item.get("Breadcrumbs", "")
        product_name = item.get("ProductName", "")

        if (re.search("Аспиратори", breadcrumbs, re.IGNORECASE) and
            not re.search("Дополнителна", breadcrumbs, re.IGNORECASE) and
            not re.search("Додатен прибор", breadcrumbs, re.IGNORECASE) and
            not re.search("Филтер", breadcrumbs, re.IGNORECASE)):
            return self.classes_list[0], self.classes_map[self.classes_list[0]]
        
        elif (re.search("Бојлери", breadcrumbs, re.IGNORECASE) or
            re.search("бојлер", product_name, re.IGNORECASE) or
            re.search("проточен бојлер", breadcrumbs, re.IGNORECASE) or
            re.search("Електрична чешма", breadcrumbs, re.IGNORECASE) or
            re.search("Електрична батерија", breadcrumbs, re.IGNORECASE) or
            re.search("Батерија високомонтажна", breadcrumbs, re.IGNORECASE) or
            re.search("Батерија нискомонтажна", breadcrumbs, re.IGNORECASE) or
            re.search("проточна", breadcrumbs, re.IGNORECASE) or
            re.search("елек.батерија", breadcrumbs, re.IGNORECASE)):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]
        
        else:
            return None, None
    

    def generate_structure(self, item):
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
    "Tип": "Аспиратор",
    "Mарка": "име на бренд",
    "Tежина кг": број во кг,
    "Mоќност W": врој во W,
    "Kапацитет л": број во литри,
    "Ниво на бучава dB": број во dB,            
    "материјал": " инокс",                       
    "Изолација": " број во см",                                                                    
    "Максимална температура": број во °C,                                                         
    "Функции": ["Турбо режим", "LED осветлување"],                                                                                              
    "Монтажа": "Внатрешна",                      
    "Боја": "Сива",                           
    "Контроли": "Термостат",                                                                     
    "Вшмукувачка моќ m³/h": број во m³/h,                                   
    "Осветлување": "LED",                                   
    "Дијаметар на одводно црево см": број во см,                      
    "Филтери": "HEPA",                                        
    "Димензија": [ширина, висина, длабочина] во мм            
    }}

    # ПРАВИЛА ЗА КЛУЧЕВИТЕ:
    # - "Тип": "Име на типот на производ (Аспиратор или Бојлер)",
    # - "Марка": "името на бренд",
    # - "Тежина кг": тежина на производот во кг,
    # - "Моќност W": моќност во W,
    # - "Капацитет л": капацитет во литри,
    # - "Ниво на бучава dB": ниво на бучава во dB,            
    # - "Материјал": " инокс",                       
    # - "Изолација": " видот на изолација и димензијата на истата во см",                                                                    
    # - "Максимална температура": број во °C,                                                         
    # - "Функции": ["Турбо режим", "LED осветлување"],                                                                                              
    # - "Монтажа": "Начин на монтажа (Внатрешна, Надворешна, високо монтажна, итн)",                      
    # - "Боја": "боја на производот (Сива, Бела, Црна, итн)",                           
    # - "Контроли": "начин на контроли (Термостат, Електронски, итн)",                                                                     
    # - "Вшмукувачка моќ m³/h": моќност на вшмукување во m³/h,                                   
    # - "Осветлување": "начин на осветлување (LED, Халогенско, итн)",                                   
    # - "Дијаметар на одводно црево см": ширина на цревото (дијаметар) во см,                      
    # - "Филтери": "HEPA",                                        
    # - "Димензија": [ширина, висина, длабочина] во мм  
    # РЕЗУЛТАТ: Врати исклучиво чист JSON објект.
    """


        pass
evaluator = Evaluation(ClassifierOstanato())
evaluator.evaluate_All_products()
