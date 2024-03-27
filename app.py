from flask import Flask, request, render_template, jsonify, make_response, session
import numpy as np
import pickle
import jwt
import datetime
with open('logreg.pkl', 'rb') as file:
    model=pickle.load(file)
    
app=Flask(__name__)

app.config['SECRET_KEY']='secretkey'

@app.route("/login")
def login():

    authentication=request.authorization

    if authentication and authentication.password== 'password':
        web_token_expire=str(datetime.datetime.now(tz=datetime.timezone.utc)+ datetime.timedelta(minutes=15))
        web_token=jwt.encode({'user': authentication.username, 
                              'web_token_expire':web_token_expire},
                                app.config['SECRET_KEY'] )
        
        return jsonify({'web_token': web_token})
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/predict", methods=["POST"])
def predict_diabetes():
   
    features= [float(x) for x in request.form.values()]
    feature_names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
       'BMI', 'DiabetesPedigreeFunction', 'Age']
    final_features=[np.array(features)]
    prediction=model.predict(final_features)
    probabilty=model.predict_proba(final_features)
    diabetes_probabilty=probabilty[0][1]

    prediction=model.predict(final_features)
    
    output= prediction[0]
    
    if output==1:
        return render_template('index.html', prediction_text=f"Based on the given values, it is with probability of {diabetes_probabilty*100:.2f}% that this person likly to have diabetes ")
    else:
        return render_template('index.html', prediction_text=f"Based on the given values, it is with probability of {diabetes_probabilty*100:.2f}% that this person likly to have diabetes ")

if __name__=="__main__":
    app.run(debug=True)