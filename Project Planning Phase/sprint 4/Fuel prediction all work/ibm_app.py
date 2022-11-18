import flask
import joblib
import requests
from flask import render_template, request
from flask_cors import CORS

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "l1fzrxmeL6hj7RAtabNLi7eiu0d83k8cthPzcjr21q52"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET'])
def sendHomePage():
    return render_template("prediction.html")

@app.route('/y_predict', methods=['POST'])
def y_predict():
    distance = float(request.form['distance'])
    speed = int(request.form['speed'])
    tem_outside = int(request.form['tem_outside'])
    gas_type = int(request.form['gas_type'])
    rain = int(request.form['rain'])
    sun = int(request.form['sun'])

    X  = [[distance, speed, tem_outside,gas_type,rain,sun]]

    payload_scoring = {"input_data": [{"field": [['distance', 'speed', 'tem_outside', 'gas_type','rain','sun']], "values": X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/50f7f5a7-b0e4-458f-9f9f-6eb5edb9936f/predictions?version=2022-11-11', json=payload_scoring,headers={'Authorization': 'Bearer ' + mltoken})

    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    return render_template("prediction.html",prediction_text=predict)
   

if __name__ == '__main__':
    app.run()
