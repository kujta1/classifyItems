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
        
        elif re.search("Бојлери", breadcrumbs, re.IGNORECASE):
            return self.classes_list[1], self.classes_map[self.classes_list[1]]
        
        else:
            return None, None
        
    def generate_structure(self, item):
    
        """
        Генерирај ја структурирана JSON структура за производот врз основа на неговиот опис.            
        
        JSON структура:
        {
            "тип на производ": string,
            "компоненти": [
                {
                    "тип": string,                                      
                    "материјал": string | null,                       
                    "изолација": string | null,                       
                    "тежина кг": number | null,                          
                    "моќност W": number | null,                           
                    "притисок": string | null,                           
                    "максимална температура": number | null,                                                         
                    "функции": [string],                                
                    "капацитет л": number | null,                                                                
                    "монтажа": string | null,                      
                    "боја": string | null,                           
                    "контроли": string | null,                                    
                    "ниво на бучава dB": number | null,                                 
                    "вшмукувачка моќ m³/h": number | null,                                   
                    "осветлување": string | null,                                   
                    "дијаметар на одводно црево см": number | null,                      
                    "филтери": string | null,                                        
                    "димензии мм": {
                        "ширина": number | null,                          
                        "висина": number | null,                   
                        "длабочина": number | null                   
                    } 
                }
            ]
        }           

        ВЛЕЗ: {item}
        """ 

    # Prepare structured output
        structured_data = {
        "тип на производ": self.classify(item)[0] if self.classify(item)[0] else "other",
        "компоненти": [
            {
                "тип": item.get("ProductName", None), 
                "материјал": None,  
                "изолација": None,  
                "тежина кг": None,  
                "моќност W": None,  
                "притисок": None, 
                "максимална температура": None,  
                "функции": [],  
                "капацитет л": None,  
                "монтажа": None, 
                "боја": None, 
                "контроли": None, 
                "ниво на бучава dB": None,  
                "вшмукувачка моќ m³/h": None,  
                "осветлување": None,  
                "дијаметар на одводно црево см": None,  
                "филтери": None, 
                "димензии мм": {
                    "ширина": None,  
                    "висина": None,  
                    "длабочина": None  
                }
            }
        ]
    }

    # Extract relevant features from the Description
        description = item.get("Description", "")
       # Extract relevant features from the Description
        if description:
            # Example: Extracting dimensions
            dimensions_match = re.search(r'(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)\s*x\s*(\d+(\.\d+)?)', description)
            if dimensions_match:
                structured_data["компоненти"][0]["димензии мм"]["ширина"] = float(dimensions_match.group(1))
                structured_data["компоненти"][0]["димензии мм"]["висина"] = float(dimensions_match.group(3))
                structured_data["компоненти"][0]["димензии мм"]["длабочина"] = float(dimensions_match.group(5))
            
            # Extracting the capacity
            capacity_match = re.search(r'Капацитет:\s*(\d+(?:,\d+)?)\s*л', description)
            if capacity_match:
                structured_data["компоненти"][0]["капацитет л"] = float(capacity_match.group(1).replace(',', '.'))  # Handle decimal

            # Extracting weight
            weight_match = re.search(r'\бтежина\b.*?(\d+(\.\d+)?)\s*кг', description)
            if weight_match:
                structured_data["компоненти"][0]["тежина кг"] = float(weight_match.group(1))

            # Extracting power
            power_match = re.search(r'\bмоќност\b.*?(\d+(\.\d+)?)\s*W', description)
            if power_match:
                structured_data["компоненти"][0]["моќност W"] = float(power_match.group(1))

            # Extracting noise level
            noise_match = re.search(r'\bниво на бучава\b.*?(\d+(\.\d+)?)\s*dB', description)
            if noise_match:
                structured_data["компоненти"][0]["ниво на бучава dB"] = float(noise_match.group(1))
            
            # Extracting additional features from description
            functions = re.findall(r'\bфункција\b.*?:\s*(.*?)\s*(?=,\s*\S|$)', description)  # Example to extract functions
            structured_data["компоненти"][0]["функции"] = [func.strip() for func in functions]

            return structured_data
        pass
evaluator = Evaluation(ClassifierOstanato())
evaluator.evaluate_All_products()