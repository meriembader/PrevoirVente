from flask import Flask, request, render_template
import pandas as pd
import pickle as p
import numpy as np
from flask_cors import CORS
import warnings
import csv
from bson.json_util import dumps
from bson import Binary, Code
import pymongo
from pymongo import MongoClient
from  connexionBD import *
import openpyxl
from sklearn.metrics import mean_squared_error, mean_absolute_error
from flask import send_file
app = Flask(__name__,template_folder='templates')
CORS(app)

warnings.filterwarnings("ignore")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["dataEra"]
#Loading the model
model = p.load(open('model.h5', 'rb'))

@app.route('/', methods=['GET','POST'])
def home():
  return render_template('upload.html')


@app.route('/predict', methods=['Get','POST'])
def predict():
     if request.method== 'POST':
            file = request.files['file']
            print('file=',file.filename)
     
            sales_data=pd.read_excel(file)
            sales_data.drop(['OrderDateKey','DueDateKey','ShipDateKey','CustomerKey','PromotionKey'],axis=1,inplace=True)
            sales_data.drop(['CurrencyKey','SalesTerritoryKey','SalesOrderNumber','CustomerPONumber'],axis=1,inplace=True)
            sales_data.drop(['CarrierTrackingNumber'],axis=1,inplace=True)
          
            sales_data['OrderDate']=pd.to_datetime(sales_data['OrderDate'], format='%Y-%m-%d %H:%M:%S')

            sales_data.head(7)

            sales_data['OrderDate'] = sales_data['OrderDate'].dt.year.astype('str')+'-'+sales_data['OrderDate'].dt.month.astype('str')+'-01'
            sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'])
           
            sales_data.head(7)

            predict_sales_data = sales_data.groupby('OrderDate')['OrderQuantity','SalesAmount'].sum()
            
            forecast_t=np.round(model.predict(start = len(predict_sales_data)-12,
                                     end = len(predict_sales_data)+11,

                                     typ = 'levels').rename('Forecast'),0)
            frame = { 'Date': forecast_t.index, 'forecast': forecast_t }
            result = pd.DataFrame(frame)

            rmse=np.sqrt(mean_squared_error(predict_sales_data['OrderQuantity'].tail(12),forecast_t.head(12)))

          
            result.to_excel(r'Forecast.xlsx',index=False)
            df2 = pd.read_excel(r'C:\Users\Meriem\Desktop\Stage_Data-Era_2020\prevoir_vente\Forecast.xlsx')
            x = pd.concat([sales_data, df2], axis=1)
            cols = ['UnitPrice', 'ExtendedAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount', 'TaxAmt', 'Freight']
            #for col in cols:
            #    x[col] = x[col].apply(lambda y: str(y).replace('.',','))
            x.to_csv(r'result.csv',header=True, sep = ';', index=False)

            #connexion_base
            insert_csv('result.csv')

           # df1 = pd.read_excel(r'C:\Users\Meriem\Desktop\Stage_Data-Era_2020\prevoir_vente\fact_internetsales1.xls')
            #df2 = pd.read_excel(r'C:\Users\Meriem\Desktop\Stage_Data-Era_2020\prevoir_vente\Forecast.xlsx')
            #x = pd.concat([sales_data, df2], axis=1)
           # x.to_excel(r'result.xlsx',header=True)
            return render_template('result.html')

from connexionBD import mydb
import json
from flask import jsonify
from flask import Response
import pprint
@app.route("/api/test",  methods=['GET'])
def stat():


  variab = mydb.tt.aggregate([

       { "$group": { "_id": "$ProductKey","UnitPrice": {"$sum":1}  }}])

  json_string = json.dumps(list(variab))
  print('varjson', json_string)
  return  json_string

@app.route("/api/test1",  methods=['GET'])
def stat1():


  variab1 = mydb.tt.aggregate([

       { "$group":  { "_id": "$OrderDate","Freight": {"$sum":1} }}])

  json_string = json.dumps(list(variab1))
  print('varjson', json_string)
  return  json_string

@app.route("/api/test2",  methods=['GET'])
def stat2():


  variab2 = mydb.tt.aggregate([

       { "$group": { "_id": "$DueDate","SalesAmount": {"$sum":1}}}])

  json_string = json.dumps(list(variab2))
  print('varjson', json_string)
  return  json_string


@app.route("/api/test3",  methods=['GET'])
def stat3():


  variab2 = mydb.tt.aggregate([

        { "$group": { "_id": "$ShipDate","TaxAmt": {"$sum":1}}}])

  json_string = json.dumps(list(variab2))
  print('varjson', json_string)
  return  json_string

  
@app.route("/api/test4",  methods=['GET'])
def stat4():
  variab2 = mydb.tt.find(
    { },
    { "forecast": 1, "Date": 1, "_id":0 }).limit(24)
  json_string = json.dumps(list(variab2))
  print('varjson', json_string)
  return  (json_string)

@app.route("/api/test5",  methods=['GET'])
def stat5():
 variab2 = list(mydb.tt.aggregate([
              { "$group": { "_id": "$OrderDate","OrderQuantity": {"$sum":1}}},
              { "$sort" : { "_id" : 1 } }
  ]))
 json_string = json.dumps(list(variab2))
 print('forecast', json_string)
 return  (json_string)

  
  #var = variab.object().to_json()
  #print('var2', var)

   #Response(list(variab), mimetype="application/json", status=200)


 # return jsonify( { 'result': mydb.mytable.aggregate([
  #      { "$group": {"_id": "$status", "author": { '$sum': 1}}}])})

if __name__ == '__main__':
    app.run(port=5000, debug=True)



    