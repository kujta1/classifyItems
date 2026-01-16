import re
from classifier import Classifier
from evaluate import Evaluation

class ClassifierShporeti(Classifier):
    def __init__(self, classes_list=None, classes_map=None):
        """
        ClassifierShporeti
        Овој класификатор е наменет за класификација на производи
        од доменот шпорети, вградливи уреди и микробранови печки.

        Главниот извор на информација е полето Breadcrumbs, а како
        резервен механизам се анализираат ProductName и
        FormattedDescription. На овој начин се подобрува точноста
        и се намалува зависноста од структурираноста на веб продавниците.
        """

        """
        Класификатор за:
        - Шпорети
        - Вградливи сетови од рерна и плотна
        - Вградливи фурни и плотни
        - Микробранови печки
        - Вградливи плотни
        - Вградливи рерни
        """

        if classes_list is None:
            classes_list = [
                "67f71a03523d00258894a4de",  # Шпорети
                "67f71a03523d00258894a4e2",  # Вградливи сетови од рерна и плотна
                "67f71a03523d00258894a4d6",  # Вградливи фурни и плотни
                "67f71a03523d00258894a4e3",  # Микробранови печки
                "67f71a03523d00258894a4e1",  # Вградливи плотни
                "67f71a03523d00258894a4e0",  # Вградливи рерни
            ]

        if classes_map is None:
            classes_map = {
                "67f71a03523d00258894a4de": "Шпорети",
                "67f71a03523d00258894a4e2": "Вградливи сетови од рерна и плотна",
                "67f71a03523d00258894a4d6": "Вградливи фурни и плотни",
                "67f71a03523d00258894a4e3": "Микробранови печки",
                "67f71a03523d00258894a4e1": "Вградливи плотни",
                "67f71a03523d00258894a4e0": "Вградливи рерни",
            }

        super().__init__(classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        """
        Класификација на шпорети / вградливи уреди / микробранови.

        1) Прво гледаме 'Breadcrumbs' – најчист сигнал за категорија.
        2) Ако таму нема ништо релевантно, правиме fallback на
           ProductName + FormattedDescription и бараме клучни зборови.
        3) Редоследот е од поспецифични кон погенерални фрази за да
           избегнеме преклопувања (пример: 'вградливи фурни и плотни'
           пред 'вградливи плотни').
        """

        breadcrumbs = (item.get("Breadcrumbs") or "").lower()
        name = (item.get("ProductName") or "").lower()
        formatted = (item.get("FormattedDescription") or "").lower()
        text = f"{name} {formatted}"

        # -----------------------------
        # 1) Breadcrumbs логика
        # -----------------------------

        # Вградливи сетови од рерна и плотна
        if "вградливи сетови од рерна и плотна" in breadcrumbs:
            cat_id = self.classes_list[1]
            return cat_id, self.classes_map[cat_id]

        # Вградливи фурни и плотни
        if "вградливи фурни и плотни" in breadcrumbs:
            cat_id = self.classes_list[2]
            return cat_id, self.classes_map[cat_id]

        # Вградливи микробранови печки
        if "вградливи микробранови печки" in breadcrumbs:
            cat_id = self.classes_list[3]
            return cat_id, self.classes_map[cat_id]

        # Микробранови печки
        if "микробранови печки" in breadcrumbs:
            cat_id = self.classes_list[3]
            return cat_id, self.classes_map[cat_id]

        # Вградливи плотни
        if "вградливи плотни" in breadcrumbs:
            cat_id = self.classes_list[4]
            return cat_id, self.classes_map[cat_id]

        # Вградливи рерни
        if "вградливи рерни" in breadcrumbs:
            cat_id = self.classes_list[5]
            return cat_id, self.classes_map[cat_id]

        # Шпорети
        if "шпорети" in breadcrumbs:
            cat_id = self.classes_list[0]
            return cat_id, self.classes_map[cat_id]

        # -----------------------------
        # 2) FALLBACK: име + опис
        # -----------------------------

        # Микробранова печка
        if ("микро" in text or "микробранов" in text or "microwave" in text) and "печк" in text:
            cat_id = self.classes_list[3]
            return cat_id, self.classes_map[cat_id]

        # Вградна рерна
        if "вградн" in text and "рерна" in text:
            cat_id = self.classes_list[5]
            return cat_id, self.classes_map[cat_id]

        # Вградна плотна / плоча
        if "вградн" in text and ("плотна" in text or "плоча" in text):
            cat_id = self.classes_list[4]
            return cat_id, self.classes_map[cat_id]

        # Сет: рерна + плотна
        if "сет" in text and "рерна" in text and ("плотна" in text or "плоча" in text):
            cat_id = self.classes_list[1]
            return cat_id, self.classes_map[cat_id]

        # Вградлива фурна + плотна
        if "фурна" in text and ("плотна" in text or "плоча" in text) and "вград" in text:
            cat_id = self.classes_list[2]
            return cat_id, self.classes_map[cat_id]

        # Шпорет (електричен, комбиниран...)
        if "шпорет" in text or "cooker" in text:
            cat_id = self.classes_list[0]
            return cat_id, self.classes_map[cat_id]

        # Ништо не одговара → останато
        return None, None

    def generate_structure(self, item: dict) -> dict:
        """
        Генерира структуриран оутпут (карактеристики) за даден производ
        од класата шпорети / вградливи уреди / микробранови.

        Идеја:
        - Како влез користиме најструктуриран текст што го имаме:
          FormattedDescription (ако постои), инаку Description и ProductName.
        - Враќаме dict со клучеви (brand, model, power_w, capacity_l, dimensions_cm, ...)
          кои можат понатаму да се користат за препораки или филтрирање.

        Во реална имплементација, овде би повикале генеративно БИ (LLM, на пр. Groq),
        на кое би му го пратиле описот на производот и би барале JSON како одговор.
        Подолу прво е даден пример со регуларни изрази (детерминистичка логика),
        а во коментар е прикажано како би изгледал пример со LLM.
        """

        # 1) Подготовка на текстот за анализа:
        #    - FormattedDescription најчесто е "исчистена" верзија
        #    - ако го нема, паѓаме на Description / ProductName.
        formatted = (item.get("FormattedDescription") or "").strip()
        description = (item.get("Description") or "").strip()
        name = (item.get("ProductName") or "").strip()

        # Го спојуваме сето во еден текст за анализа
        # (го користиме lower() за полесно пребарување)
        full_text = f"{name}\n{formatted}\n{description}".lower()

        # 2) Почетна структура: сите полиња се None / default.
        #    Ова е "schema" за нашите карактеристики.
        structure = {
            "raw_name": name,
            "raw_formatted_description": formatted,
            "category_human": None,  # пример: "микробранова печка", "вградна рерна"
            "brand": None,  # пример: "Gorenje", "Vivax", "Bosch"
            "model": None,  # пример: "BM 201 AG1X"
            "built_in": False,  # дали е вградлив уред
            "power_w": None,  # моќност во W (микро / шпорет / рерна)
            "grill_power_w": None,  # ако постои посебно за инфра грејач / грил
            "capacity_l": None,  # капацитет во литри
            "dimensions_cm": {
                "width": None,
                "height": None,
                "depth": None,
            },
            "energy_class": None,  # пример: "A", "A+", "A++"
            "color": None,  # пример: "бела", "инокс"
            "features": [],  # листа од карактеристики (AquaClean, Turbo fan...)
        }

        # 3) Brand и model (многу груба логика, но доволна за демонстрација):
        #    Често првиот збор во ProductName е бренд, вториот дел е модел.
        if name:
            # Пример: "ВГРАДНА МИКРОБРАНОВА ПЕЧКА GORENJE BM 201 AG1X"
            # или "Bosch BFL554MB0 микровална"
            tokens = name.split()
            # наоѓаме прв "латиничен" токен и го третираме како бренд
            latin_tokens = [t for t in tokens if re.search(r"[a-zA-Z]", t)]
            if latin_tokens:
                structure["brand"] = latin_tokens[0]
                # остатокот може да се смета за модел (споен во стринг)
                model_tokens = latin_tokens[1:]
                if model_tokens:
                    structure["model"] = " ".join(model_tokens)

        # 4) Проверка дали е вградлив уред
        if "вградн" in full_text:
            structure["built_in"] = True

        # 5) Категорија (микробранова, шпорет, рерна, плотна)
        if "микро" in full_text or "микробранов" in full_text or "microwave" in full_text:
            structure["category_human"] = "микробранова печка"
        elif "шпорет" in full_text or "cooker" in full_text:
            structure["category_human"] = "шпорет"
        elif "рерна" in full_text or "фурна" in full_text:
            structure["category_human"] = "рерна / фурна"
        elif "плотна" in full_text or "плоча" in full_text:
            structure["category_human"] = "плотна"

        # 6) Моќност (пример: "800 W", "2500W")
        power_match = re.search(r"(\d+)\s*W", full_text)
        if power_match:
            try:
                structure["power_w"] = int(power_match.group(1))
            except ValueError:
                pass

        # 7) Капацитет во литри (пример: "20 l", "65л", "65 L")
        capacity_match = re.search(r"(\d+)\s*(l|л)\b", full_text)
        if capacity_match:
            try:
                structure["capacity_l"] = int(capacity_match.group(1))
            except ValueError:
                pass

        # 8) Димензии (пример: "595x388x325 mm" или "60x44x47cm")
        dim_match = re.search(
            r"(\d+)\s*[x×]\s*(\d+)\s*[x×]\s*(\d+)\s*(cm|мм|mm)", full_text
        )
        if dim_match:
            try:
                w = int(dim_match.group(1))
                h = int(dim_match.group(2))
                d = int(dim_match.group(3))
                structure["dimensions_cm"]["width"] = w
                structure["dimensions_cm"]["height"] = h
                structure["dimensions_cm"]["depth"] = d
            except ValueError:
                pass

        # 9) Енергетска класа (пример: "енергетска класа: A+", "класа A")
        energy_match = re.search(r"енергетска класа[:\s]*([A-G][+]{0,2})", full_text)
        if energy_match:
            structure["energy_class"] = energy_match.group(1)

        # 10) Боја (многу грубо – бараме клучни зборови)
        if "бела" in full_text:
            structure["color"] = "бела"
        elif "инокс" in full_text or "inox" in full_text:
            structure["color"] = "инокс"
        elif "црна" in full_text:
            structure["color"] = "црна"

        # 11) Клучни features / технологии (пример: AquaClean, Turbo fan)
        features = []
        if "aquaclean" in full_text:
            features.append("AquaClean")
        if "turbo fan" in full_text or "turbo ventilator" in full_text:
            features.append("Turbo fan")
        if "smartdisplay" in full_text or "smart display" in full_text:
            features.append("SmartDisplay")
        if "заклучување за заштита од деца" in full_text or "детско заклучување" in full_text:
            features.append("Child lock")

        structure["features"] = features

        # ------------------------------------------------------------------
        # 12) Пример како би изгледало со генеративно БИ (LLM)
        # ------------------------------------------------------------------
        # Во реален систем, наместо рачно да ги пишуваме сите regex правила,
        # би користеле LLM (на пр. Groq, OpenAI и сл.) со промпт од тип:
        #
        # prompt = f"""
        # Извади структуриран JSON со карактеристиките на овој уред
        # (brand, model, category_human, power_w, capacity_l, dimensions_cm,
        #  energy_class, color, features[]) од следниот опис:
        #
        # {full_text}
        #
        # Врати само валиден JSON без дополнителен текст.
        # """
        #
        # client = Groq(api_key=GROQ_API_KEY)
        # response = client.chat.completions.create(
        #     model="llama3-8b-8192",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.2,
        #     response_format={"type": "json_object"},
        # )
        # llm_struct = json.loads(response.choices[0].message.content)
        # return llm_struct
        #
        # За потребите на оваа задача, го задржуваме детерминистичкиот
        # (regex) пристап и враќаме structure.

        return structure


evaluator = Evaluation(ClassifierShporeti())
evaluator.evaluate_All_products()


"""
Евалуација и споредба на алгоритми за класификација

Во првата верзија алгоритмот класификацијата се базираше исклучиво на полето Breadcrumbs.
Овој пристап работи само кога веб продавницата користи коректна и конзистентна структура
на категории. Во случаите кога Breadcrumbs не содржат точна категорија (или производот
е погрешно означен), алгоритмот не може да класифицира.

Како резултат на тоа, правилно беа класифицирани 1341 производи, додека 64 останаа
или некласифицирани или погрешно класифицирани.

Во втората верзија се воведоа дополнителни правила кои ги анализираат текстуалните
полиња ProductName и FormattedDescription. На овој начин алгоритмот повеќе не зависи
само од Breadcrumbs, туку го користи и описниот текст на производот.

Со ова значително се зголеми бројот на точно класифицирани производи од 1341 на 1554,
што претставува зголемување од околу 16%.

Новата верзија идентификува и голем број производи кои во dataset-от се категоризирани
како „Останато од бела техника“, но според описот и името всушност припаѓаат во категоријата
„Микробранови печки“. На овој начин алгоритмот дополнително ги коригира грешките што ги
внесуваат веб продавниците во структурата на податоците.

Бројот на погрешно класифицирани производи се зголемува од 64 на 76, што претставува
мала цена за добиеното зголемување на покриеноста и точноста на класификацијата.
Најчесто грешките настануваат кога зборови како „вградна“, „печка“ или „плотна“
се појавуваат во опис на производ кој сепак не припаѓа на овие категории.

Заклучок: новата верзија на алгоритмот е значително покорисна за реална примена,
бидејќи правилно класифицира многу поголем број производи и истовремено исправува
постоечки грешки во dataset-от, додека бројот на новонастанати грешки останува релативно мал.
"""



