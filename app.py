from flask import Flask, request, render_template
import pandas as pd
import pickle as p
import numpy as np
from flask_cors import CORS
import warnings
import csv
from sklearn.metrics import mean_squared_error, mean_absolute_error
import openpyxl
import pymongo
from pymongo import MongoClient
from connexionBD import *

app = Flask(__name__,template_folder='templates')
CORS(app)

warnings.filterwarnings("ignore")

#Loading the model
model = p.load(open('model.h5', 'rb'))

@app.route('/', methods=['GET','POST'])
def home():
  return render_template('upload.html')


@app.route('/predict', methods=['Get','POST'])

def predict():
     if request.method== 'POST':
            file = request.files['file']
            print('The file is : ', request.files['file'])
            print('file=',file.filename)
            #processing
            sales_data=pd.read_excel(file)
            sales_data.drop(['OrderDateKey','DueDateKey','ShipDateKey','CustomerKey','PromotionKey'],axis=1,inplace=True)
            sales_data.drop(['CurrencyKey','SalesTerritoryKey','SalesOrderNumber','CustomerPONumber'],axis=1,inplace=True)
            sales_data.drop(['CarrierTrackingNumber'],axis=1,inplace=True)
            #print(sales_data.info())
            sales_data['OrderDate']=pd.to_datetime(sales_data['OrderDate'], format='%Y-%m-%d %H:%M:%S')

            sales_data.head(7)

            sales_data['OrderDate'] = sales_data['OrderDate'].dt.year.astype('str')+'-'+sales_data['OrderDate'].dt.month.astype('str')+'-01'
            sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'])
            #print(sales_data.info())
            sales_data.head(7)

            predict_sales_data = sales_data.groupby('OrderDate')['OrderQuantity','SalesAmount'].sum()
            #print(predict_sales_data)

            #predicting

            forecast_t=np.round(model.predict(start = len(predict_sales_data)-12,
                                     end = len(predict_sales_data)+11,
                                     typ = 'levels').rename('Forecasting of quantity order'),0)

            rmse=np.sqrt(mean_squared_error(predict_sales_data['OrderQuantity'].tail(12),forecast_t.head(12)))
          
            forecast_t.to_excel(r'Forecast.xls',index=True)
            
            
            df2 = pd.read_excel(r'Forecast.xls')
            x = pd.concat([sales_data, df2], axis=1)
            cols = ['UnitPrice', 'ExtendedAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount', 'TaxAmt', 'Freight']
            #for col in cols:
            #    x[col] = x[col].apply(lambda y: str(y).replace('.',','))
            x.to_csv(r'result.csv',header=True, sep = ';')



            #connexion_base
            insert_csv('result.csv', ',')


            return render_template('result.html')



if __name__ == "__main__" :
  app.run(debug=True)
