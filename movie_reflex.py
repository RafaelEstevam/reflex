from inference_engine import Inference, Rule
import pymongo
import ex4
from ex4 import application_collection

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["ia"]
application_collection = application_db["rule"]

composite_rules = application_collection.find()
inferences = []
for composite_rule in composite_rules:
    rules = []
    rule = composite_rule['rules']
    r = Rule(rule['relation'], rule['percept_ref'], rule['percept_name'], rule['action'])
    rules.append(r)
    inferences.append(Inference(rules, composite_rule['operators'], rule['action']))

item = input("Qual foi o filme assistido? \n")
percepts = [{"movie": "'" + item + "'" }]

for inference in inferences:

    for percept in percepts:

        inference_result = inference.infer(percept)
        if inference_result != 'False':
            print(f" Filme assistido: {percept.get('movie')} \n Você pode gostar também do : {inference_result}")
