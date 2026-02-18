from flask import Flask, render_template,request
import joblib
import numpy as np
app = Flask(__name__)
model = joblib.load('random_forest_model.pkl')
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    #get input values from form 
    age_first_funding_year=float(request.form['age_first_funding_year'])
    age_last_funding_year=float(request.form['age_last_funding_year'])
    age_first_milestone_year=float(request.form['age_first_milestone_year'])
    age_last_milestone_year=float(request.form['age_last_milestone_year'])
    funding_rounds=float(request.form['funding_rounds'])
    funding_total_usd=float(request.form['funding_total_usd'])
    milestones=float(request.form['milestones'])
    relationships=float(request.form['relationships'])
    avg_participants=float(request.form['avg_participants'])
    #create alist with input values
    input_data=[age_first_funding_year,
                age_last_funding_year,
                age_first_milestone_year,
                age_last_milestone_year,
                funding_rounds,
                funding_total_usd,
                milestones,
                relationships,
                avg_participants]
    #make a prediction using loaded model
    prediction=model.predict([input_data])[0]
    #Map the prediction to a label to meaningful output
    if prediction==1:
        result ='Aquired'
    else:
        result='Closed'
    return render_template('result.html', result=result)
if __name__ == '__main__':
    app.run()