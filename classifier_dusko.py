import json
import re
from collections import Counter


def norm_text(s: str) -> str:
    if not s:
        return ""
    s = str(s).replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


class Classifier:
    def __init__(self, classes_list=None, classes_map=None):
        self.classes_list = classes_list or []
        self.classes_map = classes_map or {}

    def classify(self, item):
        return None, None


class ClassifyShporeti(Classifier):
    def __init__(self):
        classes_list = [
            "67f71a03523d00258894a4de",  # Шпорети
            "67f71a03523d00258894a4e2",  # Вградливи сетови од рерна и плотна
            "67f71a03523d00258894a4df",  # Вградливи фурни и плотни (чадор)
            "67f71a03523d00258894a4e3",  # Микробранови печки
            "67f71a03523d00258894a4e1",  # Вградливи плотни
            "67f71a03523d00258894a4e0",  # Вградливи рерни
        ]
        classes_map = {
            "67f71a03523d00258894a4de": "Шпорети",
            "67f71a03523d00258894a4e2": "Вградливи сетови од рерна и плотна",
            "67f71a03523d00258894a4df": "Вградливи фурни и плотни",
            "67f71a03523d00258894a4e3": "Микробранови печки",
            "67f71a03523d00258894a4e1": "Вградливи плотни",
            "67f71a03523d00258894a4e0": "Вградливи рерни",
        }
        super().__init__(classes_list=classes_list, classes_map=classes_map)

    def _ret(self, cid: str):
        return cid, self.classes_map.get(cid)

    def classify(self, item):
        b_raw = item.get("Breadcrumbs") or ""
        name_raw = item.get("ProductName") or ""
        desc_raw = item.get("Description") or ""
        url_raw = item.get("ProductUrl") or ""
        store = (item.get("StoreName") or "").strip().lower()

        b = norm_text(b_raw).lower()
        name = norm_text(name_raw).lower()
        desc = norm_text(desc_raw).lower()
        url = norm_text(url_raw).lower()

        # -------------------------------------------------------
        # 0) Strong URL signals (Neptun)
        # -------------------------------------------------------
        if store == "neptun":
            if "/categories/furni/" in url:
                return self._ret(self.classes_list[5])  # рерни
            if "/categories/plotni/" in url:
                return self._ret(self.classes_list[4])  # плотни

        # -------------------------------------------------------
        # 1) Microwaves
        # -------------------------------------------------------
        if (
            re.search(r"\bмикробран", b) or re.search(r"\bмикробран", name) or re.search(r"\bмикробран", desc)
            or re.search(r"\bмикропечк", b) or re.search(r"\bмикропечк", name) or re.search(r"\bмикропечк", desc)
        ):
            return self._ret(self.classes_list[3])

        # -------------------------------------------------------
        # 2) Sets / bundles first
        # -------------------------------------------------------
        if (
            re.search(r"\bвградливи\s+сетови\b", b)
            or re.search(r"\bвградни\s+сетови\b", b)
            or re.search(r"\bвградни\s+плотни\s+и\s+фурни\b", b)
            or re.search(r"\bсетови\b", b)
            or re.search(r"\bкомплети\b", b)
            or re.search(r"фурна\s*\+\s*плотна", b)
            or re.search(r"рерна\s*/\s*плоча", b)
            or re.search(r"\bвграден\s+шпорет\b", name)
        ):
            return self._ret(self.classes_list[1])

        # -------------------------------------------------------
        # 3) “Вградливи фурни и плотни” (чадор) -> ПРЕД рерни/плотни!
        # -------------------------------------------------------
        if re.search(r"вградливи\s+фурни\s+и\s+плотни", b):
            # ако има конкретно:
            if re.search(r"\bвградливи\s+плотни\b", b):
                return self._ret(self.classes_list[4])
            if re.search(r"\bвградливи\s+рерни\b", b):
                return self._ret(self.classes_list[5])

            # инаку по име/опис:
            if re.search(r"\bплотна\b|\bплоча\b|\bиндукц", name) or re.search(r"\bплотна\b|\bплоча\b|\bиндукц", desc):
                return self._ret(self.classes_list[4])
            if re.search(r"\bфурна\b|\bрерна\b", name) or re.search(r"\bфурна\b|\bрерна\b", desc):
                return self._ret(self.classes_list[5])

            return self._ret(self.classes_list[2])

        # -------------------------------------------------------
        # 4) Simple breadcrumb shortcuts (за “Фурни-”, “Плочи” итн)
        # -------------------------------------------------------
        if re.search(r"(почетна|дома).*\bфурни\b", b):
            return self._ret(self.classes_list[5])
        if re.search(r"(почетна|дома).*\bплочи\b", b):
            return self._ret(self.classes_list[4])

        # -------------------------------------------------------
        # 5) Built-in ovens
        # -------------------------------------------------------
        if (
            re.search(r"\bвградливи\s+рерни\b", b)
            or re.search(r"\bвградни\s+рерни\b", b)
            or re.search(r"\bфурни\s+за\s+вградување\b", b)
            or re.search(r"\bcategories\/furni\b", url)
            or re.search(r"\bфурна\s+за\s+вградувањ", name)
            or re.search(r"\bфурна\s+за\s+вградувањ", desc)
            or re.search(r"(почетна|дома).*вградна\s+техника.*\bрерни\b", b)
        ):
            return self._ret(self.classes_list[5])

        # -------------------------------------------------------
        # 6) Built-in hobs
        # -------------------------------------------------------
        if (
            re.search(r"\bcategories\/plotni\b", url)
            or re.search(r"\bвградливи\s+плотни\b", b)
            or re.search(r"\bвградни\s+плотни\b", b)
            or re.search(r"\bплотни\s+за\s+вградување\b", b)
            or re.search(r"(почетна|дома).*вградна\s+техника.*\bплотни\b", b)
        ):
            return self._ret(self.classes_list[4])

        # -------------------------------------------------------
        # 7) Accessories / “прибор” / “дополнителни елементи”
        # -------------------------------------------------------
        if re.search(r"\bприбор\b", b) or re.search(r"\bдодатоци\b", b) or re.search(r"\bдополнителни\s+елементи\b", b):
            # плотни accessories
            if re.search(r"(индукц|плоч|плотн|teppan|grill|скара)", name + " " + desc):
                return self._ret(self.classes_list[4])
            # рерни accessories
            if re.search(r"(рерн|фурн|плех|решетк|тава)", name + " " + desc):
                return self._ret(self.classes_list[5])
            # шпорети accessories
            if re.search(r"(шпорет|рингл|плин)", name + " " + desc):
                return self._ret(self.classes_list[0])

        # -------------------------------------------------------
        # 8) STOVES
        # -------------------------------------------------------
        if (
            re.search(r"\bшпорети\b", b)
            or re.search(r"\bшпорет\b", b)
            or re.search(r"\bелектрични\s+шпорети\b", b)
            or re.search(r"\bплински\s+шпорети\b", b)
            or re.search(r"\bкомбинирани\s+шпорети\b", b)
            or re.search(r"\bмини\s+шпорети\b", b)
            or re.search(r"\bбела\s+техника\s*-\s*шпорети\b", b)
        ):
            return self._ret(self.classes_list[0])

        # -------------------------------------------------------
        # 9) Fallback by text
        # -------------------------------------------------------
        if re.search(r"\bшпорет\b", name) or re.search(r"\bшпорет\b", desc):
            return self._ret(self.classes_list[0])

        if re.search(r"\bфурна\b|\bрерна\b", name) or re.search(r"\bфурна\b|\bрерна\b", desc):
            return self._ret(self.classes_list[5])

        if re.search(r"\bплотна\b|\bплоча\b|\bиндукц", name) or re.search(r"\bплотна\b|\bплоча\b|\bиндукц", desc):
            return self._ret(self.classes_list[4])

        return None, None


if __name__ == "__main__":
    clf = ClassifyShporeti()

    with open("products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    in_scope = [p for p in products if p.get("Category") in clf.classes_list]

    correct = 0
    wrong = 0
    mismatches = []

    for item in in_scope:
        predicted_id, predicted_name = clf.classify(item)
        labeled_id = item.get("Category")

        if predicted_id == labeled_id:
            correct += 1
        else:
            wrong += 1
            item["Category_predicted"] = predicted_id
            item["category_predicted_human_readable"] = predicted_name
            mismatches.append(item)

    print("In-scope total:", len(in_scope))
    print("Correct:", correct)
    print("Wrong:", wrong)
    if len(in_scope) > 0:
        print("Accuracy %:", round(correct / len(in_scope) * 100, 2))

    with open("razlichni_klasi_items.json", "w", encoding="utf-8") as f:
        json.dump(mismatches, f, indent=4, ensure_ascii=False)

    print("Saved mismatches to razlichni_klasi_items.json")

    bc = Counter((m.get("Breadcrumbs") or "").strip() for m in mismatches)
    print("\nTOP 20 breadcrumbs (wrong items):")
    for text, cnt in bc.most_common(20):
        print(cnt, "-", (text or "")[:120])
