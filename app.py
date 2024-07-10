from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from src.secureloan.pipeline.prediction import PredictionPipeline


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("s:/NEW/Projects/Secure_Loan/.conda/python.exe s:/NEW/Projects/Secure_Loan/main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            no_of_dependents =float(request.form['no_of_dependents'])
            education =float(request.form['education'])
            self_employed =float(request.form['self_employed'])
            income_annum =float(request.form['income_annum'])
            loan_amount =float(request.form['loan_amount'])
            loan_term =float(request.form['loan_term'])
            cibil_score =float(request.form['cibil_score'])
            residential_assets_value =float(request.form['residential_assets_value'])
            commercial_assets_value =float(request.form['commercial_assets_value'])
            luxury_assets_value =float(request.form['luxury_assets_value'])
            bank_asset_value =float(request.form['bank_asset_value'])
       
         
            data = [no_of_dependents, education,self_employed, income_annum,loan_amount,loan_term,cibil_score,residential_assets_value,commercial_assets_value,luxury_assets_value,bank_asset_value]
            data = np.array(data).reshape(1, 11)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)
            print(predict)
            if predict[0] < 0:
                 pred = 'Approved'
            elif predict[0] > 0:
                 pred = 'Not Approved'
            elif predict[0] == 0:
                 pred = 'Approved'
            else:
                 pred = 'Need More Information Connect to Agent!'


            return render_template('results.html', prediction = pred)

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)