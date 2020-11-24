from pymongo import MongoClient
from bson.son import SON
import pprint
client = MongoClient('mongodb://localhost:27017/')


mydb = client['dataa']
mycol = mydb["mytable"]
#  {"$sort": SON([("count",  ), ("_id", )])}
pipeline = [
        { "$group": {"_id": {"author": "$author", "count": {"$sum": 1}}}},
]
variab=list(mydb.mytable.aggregate([
        { "$group": {"_id": "$status", "author": { '$sum': 1}}}
]))

