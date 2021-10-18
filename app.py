from flask import Flask, render_template, request, flash, redirect
import pickle
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

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

@app.route("/generalPrediction", methods=['GET', 'POST'])
def generalPredictionPage():
    if request.method == 'POST':
        dic = {0:'itching',1:'chills',2:'joint_pain',3:'vomiting',4:'fatigue',5:'lethargy',6:'cough',7:'high_fever',8:'breathlessness',9:'sweating',10:'headache',11:'yellowish_skin',12:'dark_urine',13:'nausea',14:'loss_of_appetite',15:'abdominal_pain',16:'diarrhoea',17:'mild_fever',18:'yellow_urine',19:'yellowing_of_eyes',20:'acute_liver_failure',21:'swelling_of_stomach',22:'malaise',23:'phlegm',24:'chest_pain',25:'fast_heart_rate',26:'muscle_pain',27:'family_history',28:'rusty_sputum',29:'receiving_blood_transfusion',30:'receiving_unsterile_injections',31:'coma',32:'stomach_bleeding',33:'distention_of_abdomen',34:'history_of_alcohol_consumption',35:'fluid_overload.1'}
        user_list = (request.form.getlist("mycheckbox"))
        if user_list == []:
            message = "Select atleast one symptom"
            return render_template("general_prediction.html", message = message)
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
        print("the pred=", pred)
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
            values = list(map(float, list(to_predict_dict.values())))
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
                print("x=", x)
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
            # if answer == 0:
            #     return "Hepatitis is confirmed. High risk of serious illness or death."
            # elif answer == 1:
            #     return "No worries, the disease might be in its early stages.Consult a doctor as early as possible."
                    
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
        except:
            message = "Please upload an Image"
            return render_template('pneumonia.html', message = message)
    return render_template('pneumonia_predict.html', pred = pred)

if __name__ == '__main__':
	app.run(debug = True)