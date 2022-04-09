import pandas as pd
from apriori_2_algorithm import *
import pymongo

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["ia"]
application_collection = application_db["rule"]

basket_data = pd.read_csv('foo.csv')
items_by_transaction = basket_data.groupby('play')['movie'].apply(set)
itemset = basket_data['movie'].unique()
# print('Itemset: ', itemset)

rules = apriori_2(itemset, items_by_transaction, 0.02, 0.1)

composite_rule = []

for rule in rules[1]: 

    percept = rule['rule'].split('==>')[0].replace(" ", "")
    action = rule['rule'].split('==>')[1].replace(" ", "")

    newRule = {'relation':"==", 'percept_ref': "'" + percept + "'", 'percept_name': "movie", 'action': "'" + action + "'"}
    application_collection.insert_one({
        'rules': newRule,
        'operators': []
    })