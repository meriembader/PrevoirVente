import pymongo
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
from bson import Binary, Code
client = MongoClient('mongodb://localhost:27017/')
mydb = client['test1']
mycol = mydb["tt"]
def insert_csv(filepath):
    df = pd.read_csv(filepath,encoding = 'ISO-8859-1', delimiter=';') # loading csv file
    mydb['tt'].insert_many(df.to_dict('records'))


pipeline = [
        { "$group": { "_id": "$ProductKey","UnitPrice": {"$sum":1}}}]

variab=list(mydb.tt.aggregate([
        { "$group": { "_id": "$ProductKey","UnitPrice": {"$sum":1}}}
])),
pipeline = [
        { "$group":  { "_id": "$OrderDate","Freight": {"$sum":1}}}]

variab=list(mydb.tt.aggregate([
        { "$group": { "_id": "$OrderDate","Freight": {"$sum":1}}} 
])),
pipeline = [
        { "$group":  { "_id": "$DueDate","SalesAmount": {"$sum":1}}
}]

variab=list(mydb.tt.aggregate([
        { "$group": { "_id": "$DueDate","SalesAmount": {"$sum":1}}
}
])),

pipeline = [
        { "$group":  { "_id": "$ShipDate","TaxAmt": {"$sum":1}}
}]

variab=list(mydb.tt.aggregate([
        { "$group": { "_id": "$ShipDate","TaxAmt": {"$sum":1}}
}

  
])),
pipeline = [
            { "$group":  { "_id": "$DueDate","SalesAmount": {"$sum":1}}},
             { "$sort" : { "OrderDate" : 1 } }
             ]
variab=list(mydb.sales_table.aggregate([
            { "$group": { "_id": "$OrderDate","OrderQuantity": {"$sum":1}}},
             { "$sort" : { "_id" : 1 } }
])),


variab=list(mydb.tt.find(
    { },
    { "forecast": 1, "Date": 1, "_id":0 }).limit(24))








