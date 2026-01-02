from classifier import Classifier
from evaluate import Evaluation

class ClassifierOstanato(Classifier):
    def __init__(self, classes_list=["id_bojleri",
                                     "id_aspiratori",
                                     ], classes_map={
        "id_bojleri": "bojleri",
        "id_aspiratori": "Aspiratori",
    }
    ):
        super().__init__(
            classes_list=classes_list, classes_map=classes_map)

    def classify(self, item):
        # TODO
        # Vashiot KOD TUKA

        return None, None

    def generate_structure(self, item):
        # TODO
        # Vashiot KOD TUKA

        pass
evaluator = Evaluation(ClassifierOstanato())
evaluator.evaluate_All_products()