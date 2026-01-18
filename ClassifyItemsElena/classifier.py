class Classifier():
    def __init__(self, classes_list=None, classes_map=None):
        """
        Za koi classsi napravivme classifier
        primer za classfier_mashini
        classes_list=["67f71a03523d00258894a4db",
            "67f71a03523d00258894a4da", "67f71a03523d00258894a4dc"]
        classes_map={"67f71a03523d00258894a4db":"mashini za perenje",
                     "67f71a03523d00258894a4da":"mashini za sushenje",
                     "67f71a03523d00258894a4dc":"mashini za perenje i sushenje"}

        Args:
            classes_list (_type_, optional): _description_. Defaults to None.
            classes_map (_type_, optional): _description_. Defaults to None.
        """
        self.classes_list = classes_list
        self.classes_map = classes_map

    def classify(self, item):
        pass

    def generate_structure(self, item):
        pass
        #self.groq_client = GroqClient()






























# class ClassifyAspiratoriAndBojleri(Classifier):
#     def __init__(self, classes_list=["67f71a03523d00258894a4e4",
#                                      "67f71a03523d00258894a4e5",
#                                      "67f71a03523d00258894a4e6"], 
#                 classes_map={"67f71a03523d00258894a4e4": "Аспиратори",
#                              "67f71a03523d00258894a4e5": "Бојлери"}):
#         super().__init__(classes_list, classes_map)  
    
#     def classify(self, item):
#         if re.search("Аспиратори", item.get("Breadcrumbs"), re.IGNORECASE) and not re.search("Дополнителна", item.get("Breadcrumbs"), re.IGNORECASE) and not re.search("Додатен прибор", item.get("Breadcrumbs"), re.IGNORECASE) and not re.search("Филтер" , item.get("Breadcrumbs"), re.IGNORECASE):
#                 return self.classes_list[0], self.classes_map[self.classes_list[0]]
#         elif re.search("Бојлери", item.get("Breadcrumbs"), re.IGNORECASE):
#             return self.classes_list[1], self.classes_map[self.classes_list[1]]
#         else:
#             return None, None
        
# class ClassifierOstanato(Classifier):
#     def __init__(self, classes_list=None, classes_map=None):
#         if classes_list is None:
#             classes_list = ["67f71a03523d00258894a4e4", "67f71a03523d00258894a4e5"]
#         if classes_map is None:
#             classes_map = {
#                 "67f71a03523d00258894a4e4": "Аспиратори",
#                 "67f71a03523d00258894a4e5": "Бојлери"
#             }
#         super().__init__(classes_list, classes_map)

#     def contains_keywords(self, text, keywords):
#         return any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords)

#     def classify(self, item):
#         breadcrumbs = item.get("Breadcrumbs", "")
#         product_name = item.get("ProductName", "")

#         aspirator_keywords = ["Аспиратори", "аспира"]
#         boiler_keywords = [
#             "Бојлери", "бојлер", "проточен бојлер",
#             "Електрична чешма", "Електрична батерија",
#             "Батерија високомонтажна", "Батерија нискомонтажна",
#             "проточна", "елек.батерија"
#         ]
#         exclusion_keywords = ["Додатен прибор за аспиратори", "Филтер", "Дополнителна опрема"]

#         if (self.contains_keywords(breadcrumbs, aspirator_keywords) or
#                 self.contains_keywords(product_name, aspirator_keywords)) and \
#                 not self.contains_keywords(breadcrumbs, exclusion_keywords) and \
#                 not self.contains_keywords(product_name, exclusion_keywords):
#             return self.classes_list[0], self.classes_map[self.classes_list[0]]  # Аспиратори

#         elif (self.contains_keywords(breadcrumbs, boiler_keywords) or
#               self.contains_keywords(product_name, boiler_keywords)
#               ):
#             return self.classes_list[1], self.classes_map[self.classes_list[1]]  # Бојлери

#         else:
#             return None, None

# class Evaluation():
#     def __init__(self, classifier: Classifier, path_to_categories_file: str = './categories.json'):
#         self.classifier = classifier
#         with open(path_to_categories_file, 'r', encoding='utf-8') as json_file:
#             categories_data = json.load(json_file)
#             self.all_classes = {cat["_id"]: cat["name"] for cat in categories_data}

#         # Initialize confusion matrix for evaluation
#         self.confusion_matrix = {self.classifier.classes_map[key]: {value: 0 for value in self.classifier.classes_map.values()} for key in self.classifier.classes_map}

#     def evaluate_item(self, item):
#         predicted_class, _ = self.classifier.classify(item)
#         labeled_category = item["Category"]

#         return predicted_class, labeled_category, item

#     def evaluate_All_products(self, path_to_items_file: str = './products.json'):
#         results = []
#         ista_klasa = 0
#         razlichni_klasi = 0
#         ista_klasa_items = []
#         razlichni_klasi_items = []
#         filtered_products = []

#         with open(path_to_items_file, 'r', encoding='utf-8') as file:
#             items_list = json.load(file)

#         for item in items_list:
#             predicted_class, labeled_class, item = self.evaluate_item(item)

#             # Update confusion matrix
#             if predicted_class and labeled_class in self.classifier.classes_list:
#                 actual_category = self.classifier.classes_map[labeled_class]
#                 predicted_category = self.classifier.classes_map[predicted_class]
#                 self.confusion_matrix[actual_category][predicted_category] += 1
            
#             if predicted_class is not None and predicted_class != "other":
#                 ista_klasa += 1
#                 item["Category_predicted"] = predicted_class
#                 item["category_previously_human_readable"] = self.all_classes.get(labeled_class, "other")
#                 item["category_predicted_human_readable"] = self.all_classes.get(predicted_class, "other")
#                 ista_klasa_items.append(item)
                
#                 # Store filtered products
#                 filtered_products.append(item)

#             else:
#                 razlichni_klasi += 1
#                 item["Category_predicted"] = predicted_class
#                 item["category_previously_human_readable"] = self.all_classes.get(labeled_class, "other")
#                 item["category_predicted_human_readable"] = self.all_classes.get(predicted_class, "other")
#                 razlichni_klasi_items.append(item)

#         # Write results to respective JSON files
#         with open('razlichni_klasi_items.json', 'w', encoding="utf-8") as f:
#             json.dump(razlichni_klasi_items, f, indent=4, ensure_ascii=False)

#         with open('ista_klasa_items.json', 'w', encoding="utf-8") as f:
#             json.dump(ista_klasa_items, f, indent=4, ensure_ascii=False)

#         # Write filtered products to new JSON file
#         with open('filtered_products.json', 'w', encoding="utf-8") as f:
#             json.dump(filtered_products, f, indent=4, ensure_ascii=False)

#         print("Ista klasa:", ista_klasa)
#         print("Razlichni klasi:", razlichni_klasi)

#         self.output_evaluation_table()  # Print the evaluation table

#     def output_evaluation_table(self):
#         # Print or output the confusion matrix
#         print("Confusion Matrix:")
#         for actual, predictions in self.confusion_matrix.items():
#             print(f"{actual}: {predictions}")

# def generate_structure(self, item):
#     """
#     Генерирај ја структурирана JSON структура за производот врз основа на неговиот опис.            
    
#     JSON структура:
#     {
#         "тип на производ": string,
#         "компоненти": [
#             {
#                 "тип": string,                                      
#                 "материјал": string | null,                       
#                 "изолација": string | null,                       
#                 "тежина кг": number | null,                          
#                 "моќност W": number | null,                           
#                 "притисок": string | null,                           
#                 "максимална температура": number | null,                                                         
#                 "функции": [string],                                
#                 "капацитет л": number | null,                                                                
#                 "монтажа": string | null,                      
#                 "боја": string | null,                           
#                 "контроли": string | null,                                    
#                 "ниво на бучава dB": number | null,                                 
#                 "вшмукувачка моќ m³/h": number | null,                                   
#                 "осветлување": string | null,                                   
#                 "дијаметар на одводно црево см": number | null,                      
#                 "филтери": string | null,                                        
#                 "димензии мм": {
#                     "ширина": number | null,                          
#                     "висина": number | null,                   
#                     "длабочина": number | null                   
#                 } 
#             }
#         ]
#     }           

#     ВЛЕЗ: {item}
#     """ 

#     # Prepare structured output
#     structured_data = {
#         "тип на производ": self.classify(item)[0] if self.classify(item)[0] else "other",
#         "компоненти": [
#             {
#                 "тип": item.get("ProductName", None), 
#                 "материјал": None,  
#                 "изолација": None,  
#                 "тежина кг": None,  
#                 "моќност W": None,  
#                 "притисок": None, 
#                 "максимална температура": None,  
#                 "функции": [],  
#                 "капацитет л": None,  
#                 "монтажа": None, 
#                 "боја": None, 
#                 "контроли": None, 
#                 "ниво на бучава dB": None,  
#                 "вшмукувачка моќ m³/h": None,  
#                 "осветлување": None,  
#                 "дијаметар на одводно црево см": None,  
#                 "филтери": None, 
#                 "димензии мм": {
#                     "ширина": None,  
#                     "висина": None,  
#                     "длабочина": None  
#                 }
#             }
#         ]
#     }

#     # Extract relevant features from the Description
#     description = item.get("Description", "")
#        # Extract relevant features from the Description
#     if description:
#         # Example: Extracting dimensions
#         dimensions_match = re.search(r'(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)', description)
#         if dimensions_match:
#             structured_data["компоненти"][0]["димензии мм"]["ширина"] = float(dimensions_match.group(1))
#             structured_data["компоненти"][0]["димензии мм"]["висина"] = float(dimensions_match.group(3))
#             structured_data["компоненти"][0]["димензии мм"]["длабочина"] = float(dimensions_match.group(5))
        
#         # Extracting the capacity
#         capacity_match = re.search(r'Капацитет:\s*(\d+(?:,\d+)?)\s*л', description)
#         if capacity_match:
#             structured_data["компоненти"][0]["капацитет л"] = float(capacity_match.group(1).replace(',', '.'))  # Handle decimal

#         # Extracting weight
#         weight_match = re.search(r'\бтежина\b.*?(\d+(\.\d+)?)\s*кг', description)
#         if weight_match:
#             structured_data["компоненти"][0]["тежина кг"] = float(weight_match.group(1))

#         # Extracting power
#         power_match = re.search(r'\bмоќност\b.*?(\d+(\.\d+)?)\s*W', description)
#         if power_match:
#             structured_data["компоненти"][0]["моќност W"] = float(power_match.group(1))

#         # Extracting noise level
#         noise_match = re.search(r'\bниво на бучава\b.*?(\d+(\.\d+)?)\s*dB', description)
#         if noise_match:
#             structured_data["компоненти"][0]["ниво на бучава dB"] = float(noise_match.group(1))
        
#         # Extracting additional features from description
#         functions = re.findall(r'\bфункција\b.*?:\s*(.*?)\s*(?=,\s*\S|$)', description)  # Example to extract functions
#         structured_data["компоненти"][0]["функции"] = [func.strip() for func in functions]

#     return structured_data

# evaluator = Evaluation(ClassifierOstanato())
# evaluator.evaluate_All_products()











