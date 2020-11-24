
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib, json
import datetime as dt
import itertools
from dateutil.relativedelta import *
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX 
from pmdarima import auto_arima 
from statsmodels.tsa.stattools import adfuller
import warnings
import pickle
warnings.filterwarnings("ignore")
import joblib

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

#sales_data = open(r'C:\Users\Meriem\Desktop\Stage_Data-Era_2020/fact_internetsales1.xls')
sales_data=pd.read_excel(r'C:\Users\Meriem\Desktop\Stage_Data-Era_2020/fact_internetsales1.xls')
#sales_data =pd.read_excel(url);
sales_data.drop(['OrderDateKey','DueDateKey','ShipDateKey','CustomerKey','PromotionKey'],axis=1,inplace=True)
sales_data.drop(['CurrencyKey','SalesTerritoryKey','SalesOrderNumber','CustomerPONumber'],axis=1,inplace=True)
sales_data.drop(['CarrierTrackingNumber'],axis=1,inplace=True)
print(sales_data.info())
sales_data['OrderDate']=pd.to_datetime(sales_data['OrderDate'], format='%Y-%m-%d %H:%M:%S')

sales_data.head(7)

sales_data['OrderDate'] = sales_data['OrderDate'].dt.year.astype('str')+'-'+sales_data['OrderDate'].dt.month.astype('str')+'-01'
sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'])
print(sales_data.info())

sales_data.head(7)

predict_sales_data = sales_data.groupby('OrderDate')['OrderQuantity','SalesAmount'].sum()
print(predict_sales_data)
#plot monthly sales
fig=plt.figure(0,figsize=(12,4))
ax=plt.gca()
plt.plot(predict_sales_data['OrderQuantity'])
ax.set_xlabel('Year')
ax.set_ylabel('Nomber of Orders')

#ax.set_ylabel('Total Sale Amount')
est_model_sales=auto_arima(predict_sales_data['OrderQuantity'],
                           start_p=1, start_q=1, max_p=8, max_q=8,
                           start_P=0, start_Q=0, max_P=8, max_Q=8,
                           m=12, seasonal=True, trace=True, d=1, D=1,
                           error_action='ignore', suppress_warnings=True,
                           random_state = 20, n_fits=30)
print(est_model_sales.summary())
model_t = model_t = SARIMAX(predict_sales_data['OrderQuantity'],
                             order = est_model_sales.order,
                             initialization='approximate_diffuse',
                             filter_concentrated=True,
                             seasonal_order =est_model_sales.seasonal_order) 
result_t = model_t.fit() 
result_t.save("C:/Users/Meriem/Desktop/Stage_Data-Era_2020/prevoir_vente/model.h5")
loaded_ARIMA = result_t.load("C:/Users/Meriem/Desktop/Stage_Data-Era_2020/prevoir_vente/model.h5")


forecast_t=np.round(result_t.predict(start = len(predict_sales_data)-12,
                                     end = len(predict_sales_data)+11,
                                     typ = 'levels').rename('Forecast Sales'),0)
forecast_t=np.round(result_t.predict(start = len(predict_sales_data)-12,
                                     end = len(predict_sales_data)+11,
                                     typ = 'levels').rename('Forecast Sales'),0)
result_t.plot_diagnostics(figsize=(16,8))
plt.show()
forecast_t=np.round(result_t.predict(start = len(predict_sales_data)-12,
                                     end = len(predict_sales_data)+11,
                                     typ = 'levels').rename('Forecasting of quantity order'),0)
print('je suis forecasttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
print(forecast_t)
rmse=np.sqrt(mean_squared_error(predict_sales_data['OrderQuantity'].tail(12),forecast_t.head(12)))
print(rmse)
fig, ax = plt.subplots()
fig.suptitle('Forecasting of quantity order')
predict_sales_data['OrderQuantity'].plot(figsize=(18, 6),ax=ax, legend=True) 
plt.xlabel('Year')
plt.ylabel('No. of Orders')
forecast_t.plot()

forecast_t.to_excel(r'Forecast.xlsx',index=True)