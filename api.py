# @Author: Thomas Turner <thomas>
# @Date:   2021-01-29T18:09:14+01:00
# @Email:  thomas.benjamin.turner@gmail.com
# @Last modified by:   thomas
# @Last modified time: 2021-01-30T10:16:39+01:00


from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from statsmodels.tsa.seasonal import STL
import pandas as pd
import numpy as np
import datetime as dt
import json




app = Flask(__name__)
api = Api(app)


@app.route('/events', methods = ['POST'])
def thetest():
  """
  Takes in a json file containing time series data, removes trend and seasonality performs
  """
  data = request.json
  
  base_df = pd.DataFrame.from_dict(data) #construct a base dataframe with the imported json
  base_df['t'] =base_df['t'] = pd.to_datetime(base_df['t'], format = '%Y-%m-%d').dt.date #convert 't' column to dt.date object
  base_df['v'] = pd.to_numeric(base_df['v']) #ensure values are numeric
  base_df.set_index('t', inplace=True) #set the date as the index to remove trend and seasonality from data
  temp_res = STL(base_df, period=365, robust=True)
  temp_res2 = temp_res.fit()

  tseries = pd.DataFrame({'t':temp_res2.resid.index, 'v':temp_res2.resid.values})# create new dataframe with residual data from robust STL 
  tseries['rMN'] = tseries['v'].rolling(window=140).mean() #20 week rolling average
  tseries['rSTD'] = tseries['v'].rolling(window=140).std() #20 week rolling stdev
  #capture events that are more than 3 standard deviations away from the rolling average
  tseries['flagged'] = np.select([tseries['v'] > (tseries.rMN + 3*tseries.rSTD), tseries['v'] < (tseries.rMN - 3*tseries.rSTD)],[1,-1],default=0)

  #reformat seconds since epoch to date strings output the date strings to a json and return 
  outliers = pd.to_datetime(tseries[tseries.flagged !=0]['t']).dt.strftime('%Y-%m-%d')
  out_json = outliers.to_json(orient='records')
  
  return out_json


if __name__ == "__main__":
  app.run(debug=True, port=5000, host='0.0.0.0')

"""
curl -X POST\
  -H 'Content-Type: application/json'\
  -d @test_data.json\
  http://127.0.0.1:5000/events 
"""
