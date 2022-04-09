from inference_engine import Inference, Rule
import pymongo
# import main
# from main import rules

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["ia"]
application_collection = application_db["rule"]

composite_rules = application_collection.find()
inferences = []
for composite_rule in composite_rules:

    # print(composite_rule)

    rules = []
    # print(composite_rule['rules'])
    rule = composite_rule['rules']
    # for rule in composite_rule['rules']:

    r = Rule(rule['relation'], rule['percept_ref'], rule['percept_name'], rule['action'])
    rules.append(r)
    inferences.append(Inference(rules, composite_rule['operators'], rule['action']))

# percepts = [
#     {'eccomerce_item': 'RETROSPOT HEART HOT WATER BOTTLE'},
#     {'eccomerce_item': 'SCOTTIE DOG HOT WATER BOTTLE'},
#     {'eccomerce_item': "HEART OF WICKER SMALL"},
# ]

item = input("Qual foi o filme assistido? \n")
percepts = [{"movie": "'" + item + "'" }]

for inference in inferences:

    for percept in percepts:

        # print(percept.get('movie'))

        inference_result = inference.infer(percept)
        if inference_result != 'False':
            print(f" Filme assistido: {percept.get('movie')} \n Você pode gostar também do : {inference_result}")
