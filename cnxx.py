import pymongo
import pandas as pd
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
mydb = client['test1']
mycol = mydb["test"]
def insert_csv(filepath, delimiteur):
    df = pd.read_csv(filepath,encoding = 'ISO-8859-1', delimiter=delimiteur)   # loading csv file
    mydb['test1'].insert_many(df.to_dict('records'))


