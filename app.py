from flask import Flask, render_template, request, flash, redirect, session, abort, url_for, session
import pickle
from flask.globals import current_app
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import joblib
import pyrebase
import sys
import os
from functools import wraps

app = Flask(__name__)

#Add your own details
config = {
  "apiKey": "AIzaSyBx5uTcg6EfvFjLrGkB_iYM8mh7dQRVk1U",
  "authDomain": "smartdoc-capstone.firebaseapp.com",
  "databaseURL": "https://smartdoc-capstone-default-rtdb.firebaseio.com/",
  "storageBucket": "smartdoc-capstone.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#secret key for the session
app.secret_key = os.urandom(24)

# #decorator to protect routes
def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #check for the variable that pyrebase creates
        if not auth.current_user != None:
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function


#Initialze person as dictionar+y
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
results = {"step1": "", "step2": "", "step3": []}

def add_details_to_db(values):
    db.child("users").child(session['usr']).child("user_history").push(values)
    print("values , results=", values)
    print("added details to database")
    global results
    results['step1'] = ""
    results['step2'] = ""
    results['step3'] = []
    print("after reseting the detaile=", results)


#SignIn
@app.route("/signin")
def signin():
    return render_template("signin.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    return render_template("welcome.html")
    
curr_user = ""
#login route
@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
      #get the request data
      email = request.form["username"]
      password = request.form["pass"]
      try:
        #login the user
        user = auth.sign_in_with_email_and_password(email, password)
        #set the session
        user_id = user['localId']
        # user_email = email
        user_email = user["email"]
        session['usr'] = user_id
        curr_user = session['usr']
        session["email"] = user_email

        #Get the name of the user
        data = db.child("users").get()
        person["name"] = data.val()[session['usr']]["name"]
        temp = "new_" + person["name"]
        # db.child("users").child(session['usr']).child("history")[0].set(temp)
        print("Sign In successfull!!!!!!")
        return redirect(url_for('home'))  
      
      except Exception as e:
        message = 'Wrong credentials. Please provide valid data'
        print("Error message=")
        print((e))
        # print("code=", status_code)

        print("message =", message)
        return render_template('signin.html',message = message )    
    return render_template("signin.html")




#signup route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
      #get the request form data
      email = request.form["username"]
      password = request.form["pass"]
      name = request.form["name"]
      try:
        #create the user
        auth.create_user_with_email_and_password(email, password)
        #login the user right away
        user = auth.sign_in_with_email_and_password(email, password)   
        #session
        user_id = user['localId']
        # user_email = email
        user_email = user["email"]
        session['usr'] = user_id
        curr_user = session['usr']
        session["email"] = user_email
        # history = {"1":{"step1":"pneumonia", "step2":"confirmed pneumonia","step3": "side effects"}}
        
        #Append data to the firebase realtime database
        data = {"name": name, "email": email, "user_history": {}}
        db.child("users").child(session['usr']).set(data)
        print("Signup successfull")
        return redirect(url_for('home')) 
      except Exception as e:
        # return render_template("login.html", message="The email is already taken, try another one, please" )  
        print("signup unsuccessful", e)
        return render_template('signup.html', message = "Couldn\'t Sign Up. Please check your credentials")

    return render_template("signup.html")



#logout route
@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None
    #also remove the session
    #session['usr'] = ""
    #session["email"] = ""
    session.clear()
    return redirect("/")

def predict(values, dic):
    if len(values) == 8:
        model = pickle.load(open('models/diabetes.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 26:
        model = pickle.load(open('models/breast_cancer.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 13:
        model = pickle.load(open('models/heart.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 18:
        model = pickle.load(open('models/kidney.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]
    elif len(values) == 10:
        model = pickle.load(open('models/liver.pkl','rb'))
        values = np.asarray(values)
        return model.predict(values.reshape(1, -1))[0]

@app.route("/")
def home():
    return render_template('index.html')

# @app.route("/signup")
# def signup():
#     return render_template('signup.html')

@app.route("/generalPrediction", methods=['GET', 'POST'])
def generalPredictionPage():
    if request.method == 'POST':
        global results
        dic = {0:'itching',1:'chills',2:'joint_pain',3:'vomiting',4:'fatigue',5:'lethargy',6:'cough',7:'high_fever',8:'breathlessness',9:'sweating',10:'headache',11:'yellowish_skin',12:'dark_urine',13:'nausea',14:'loss_of_appetite',15:'abdominal_pain',16:'diarrhoea',17:'mild_fever',18:'yellow_urine',19:'yellowing_of_eyes',20:'acute_liver_failure',21:'swelling_of_stomach',22:'malaise',23:'phlegm',24:'chest_pain',25:'fast_heart_rate',26:'muscle_pain',27:'family_history',28:'rusty_sputum',29:'receiving_blood_transfusion',30:'receiving_unsterile_injections',31:'coma',32:'stomach_bleeding',33:'distention_of_abdomen',34:'history_of_alcohol_consumption',35:'fluid_overload.1'}
        user_list = (request.form.getlist("mycheckbox"))
        print("user list=", user_list)
        if len(user_list) == 0:
            message = "Select atleast one symptom"
            return render_template("general_prediction.html", message = message)
        if len(user_list) == 36:
            message = "Please provide valid data"
            return render_template("general_prediction.html", message = message)
        if  ('vomiting' and 'high_fever' and 'headache' and 'diarrhoea') in user_list:
            print("Call for malaria ")
            
            results['step1'] = 'Malaria'
            return render_template('general_result.html', pred='Malaria')
        res = [0 for i in range(36)]
            # print("user_list=", user_list)
        i = 0
            # print("dic=", dic)
        for i in range(36):
            if dic[i] in user_list:
                res[i] = 1
            else:
                res[i] = 0
        DT_from_joblib = joblib.load('models/general_prediction.pkl')
        pred = DT_from_joblib.predict(np.array(res).reshape(1,-1))[0]
        # global results
        results['step1'] = pred
        print("the pred=", pred)
        print("results=", results)
        
            # pred_disease = "The predicted disease is " + pred
        return render_template('general_result.html', pred=pred)
                
            # return pred_disease
    
    return render_template('general_prediction.html')

@app.route("/hepatitisresult", methods=['GET', 'POST'])
def hepatitisResultPage():
    if request.method == 'POST':
        dic = {0:'cancer', 1:'alzheimer', 2:'heart', 3:'diabetes', 4:'asthma'}
        user_list = (request.form.getlist("mycheckbox"))
        empty = 0
        if user_list == []:
            empty = 1
        res = [0 for i in range(5)]
        i = 0
        global results
        results['step3'] = user_list
        print("results = ", results)
        add_details_to_db(results)
        print("function add details called")
        
        for i in range(5):
            if dic[i] in user_list:
                res[i] = 1
            else:
                res[i] = 0
        first = res[0]
        second = res[1]
        third = res[2]
        fourth = res[3]
        fifth = res[4]
        print("user list= ", user_list)
        print("res=", res)

        
    
        return render_template('hepatitis_side_effects.html', zero = empty, first = first, second=second, third = third, fourth = fourth, fifth = fifth)

@app.route("/pneumoniaresult", methods=['GET', 'POST'])
def pneumoniaResultPage():
    if request.method == 'POST':
        dic = {0:'cancer', 1:'alzheimer', 2:'heart', 3:'diabetes', 4:'asthma'}
        user_list = (request.form.getlist("mycheckbox"))
        empty = 0
        if user_list == []:
            empty = 1
        res = [0 for i in range(5)]
        i = 0
        global results
        results['step3'] = user_list
        print("results = ", results)
        add_details_to_db(results)
        print("function add details called")
        
        for i in range(5):
            if dic[i] in user_list:
                res[i] = 1
            else:
                res[i] = 0
        first = res[0]
        second = res[1]
        third = res[2]
        fourth = res[3]
        fifth = res[4]
        print("user list= ", user_list)
        print("res=", res)

        
    
        return render_template('pneumonia_side_effects.html', zero = empty, first = first, second=second, third = third, fourth = fourth, fifth = fifth)

@app.route("/malariaresult", methods=['GET', 'POST'])
def malariaResultPage():
    if request.method == 'POST':
        dic = {0:'cancer', 1:'alzheimer', 2:'heart', 3:'diabetes', 4:'asthma'}
        user_list = (request.form.getlist("mycheckbox"))
        empty = 0
        if user_list == []:
            empty = 1
        res = [0 for i in range(5)]
        i = 0
        global results
        results['step3'] = user_list
        print("results = ", results)
        add_details_to_db(results)
        print("function add details called")
        for i in range(5):
            if dic[i] in user_list:
                res[i] = 1
            else:
                res[i] = 0
        first = res[0]
        second = res[1]
        third = res[2]
        fourth = res[3]
        fifth = res[4]
        print("user list= ", user_list)
        print("res=", res)
        return render_template('malaria_side_effects.html', zero = empty, first = first, second=second, third = third, fourth = fourth, fifth = fifth)

@app.route("/hepatitis", methods=['GET', 'POST'])
def hepatitisPage():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            print("dictionary= ", to_predict_dict)
            lst = list(to_predict_dict.values())
            
            for i in range(len(lst)):
                if lst[i] == "":
                    message = "Kindly fill all the fields."
                    return render_template("hepatitis.html", message = message) 
            x =  to_predict_dict['gender'].lower()

            if x  == 'male':
                to_predict_dict['gender'] = 1
            else:
                to_predict_dict['gender'] = 0
            values = list(map(float, list(to_predict_dict.values())))
            print("values=", values)
            for i in range(0,3):
                values[i] = float(values[i])
            for i in range(3,len(values)):
                values[i] = int(values[i])
            res = [0 for i in range(29)]
            for i in range(0,3):
                res[i] = (values[i])
            
            j= 3
            for i in range(3,len(values)):
                x = values[i]
                # print("x=", x)
                if x == 1:
                    res[j] = 1
                    res[j+1] = 0
                elif x == 0:
                    res[j] = 0 
                    res[j+1] = 1
                else:
                    message = "Please provide valid data"
                    return render_template("hepatitis.html", message = message)
                    # return "Plese provide valid data"
                j += 2
            # print("res=", res)

            
            DT_from_joblib = joblib.load('models/hepatitis_prediction.pkl')
            pred = DT_from_joblib.predict(np.array(res).reshape(1,-1))[0]
            print("hepatitis confirm stage, pred = ", pred)
            if pred == 0:
                results['step1'] = "Hepatitis "
                results['step2'] = "Hepatitis Confirmed"
            elif pred == 1:
                results['step1'] = "Hepatitis "
                results['step2'] = "Hepatitis not confirmed"
                add_details_to_db(results)
                print("results=", results)
            
                    
            return render_template('hepatitis_result.html', pred=pred)
    except:
        message = "Please provide valid data"
        return render_template("hepatitis.html", message = message)

    return render_template('hepatitis.html')


@app.route("/new", methods=['GET', 'POST'])
def newPage():
    return render_template('new.html')

@app.route("/diabetes", methods=['GET', 'POST'])
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
def cancerPage():
    return render_template('breast_cancer.html')

@app.route("/heart", methods=['GET', 'POST'])
def heartPage():
    return render_template('heart.html')

@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')

@app.route("/liver", methods=['GET', 'POST'])
def liverPage():
    return render_template('liver.html')

@app.route("/malaria", methods=['GET', 'POST'])
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()
            to_predict_list = list(map(float, list(to_predict_dict.values())))
            pred = predict(to_predict_list, to_predict_dict)
    except:
        message = "Please enter valid Data"
        return render_template("home.html", message = message)

    return render_template('predict.html', pred = pred)

@app.route("/malariapredict", methods = ['POST', 'GET'])
def malariapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image'])
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,3))
                img = img.astype(np.float64)
                model = load_model("models/malaria.h5")
                pred = np.argmax(model.predict(img)[0])
                print("malaria  confirm stage pred = ", pred)
                if pred == 1:
                    results['step1'] = "Malaria "
                    results['step2'] = "Malaria Confirmed"
                    print("results=", results)
                elif pred == 0:
                    results['step1'] = "Malaria "
                    results['step2'] = "Malaria not confirmed"
                    add_details_to_db(results)
                    print("results=", results)
            else:
                message = "Please upload an Image"
                return render_template('malaria.html', message = message)
        except:
            message = "Please upload an Image"
            return render_template('malaria.html', message = message)
    return render_template('malaria_predict.html', pred = pred)

@app.route("/pneumoniapredict", methods = ['POST', 'GET'])
def pneumoniapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image']).convert('L')
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,1))
                img = img / 255.0
                model = load_model("models/pneumonia.h5")
                pred = np.argmax(model.predict(img)[0])
                # print("pneumonia confirm stage", pred)
                if pred == 1:
                    results['step1'] = "Pneumonia "
                    results['step2'] = "Pneumonia Confirmed"
                elif pred == 0:
                    results['step1'] = "Pneumonia "
                    results['step2'] = "Pneumonia not confirmed"
                    add_details_to_db(results)
                    print("results=", results)
        except:
            message = "Please upload an Image"
            return render_template('pneumonia.html', message = message)
    return render_template('pneumonia_predict.html', pred = pred)

if __name__ == '__main__':
	app.run(debug = True)