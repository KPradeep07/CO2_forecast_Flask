from flask import Flask, render_template, request, send_file
import jsonify
import requests
import pickle
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt



model = pickle.load(open('CO2_Forecasting_ARIMA.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/predict', methods = ["POST"])
def predict():
    if request.method=="POST":
        name= request.form["years"]
        try:
            if int(name) <= 0:
                return render_template('index.html', prediction_texts = "Pleae Enter the number greater than 0")
            
            else:
                predictions = model.forecast(int(name))
                
                Data = []
                for i in range (len(predictions)):
                    year = predictions.index.year[i]
                    value = np.round(predictions.values[i],2)
                    da = (year, value)
                    Data.append(da)
                    headings = ("Year", "Forcasted CO2 Level")
                    data = tuple(Data)
            
                return render_template('index.html', prediction_texts= "The forecasted values are", headings=headings , data=data)
                
        except ValueError:
            return render_template('index.html', prediction_texts = "Alphabets are not allowed")
    
if __name__=="__main__":
    app.run(debug=True)
