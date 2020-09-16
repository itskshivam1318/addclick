from flask import Flask, render_template,request,url_for,jsonify
import numpy as np
import pickle
import sklearn
import time
from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options 
import math

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_extension('extension.crx')

global driver
global url_timestamp

url_timestamp = {}
url_viewtime = {}
prev_url = ""

options = webdriver.ChromeOptions()
options.add_extension('extension.crx')

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")


def start():
    driver = webdriver.Chrome(executable_path = DRIVER_BIN,chrome_options=options)
    return driver

def end(driver):
    driver = driver.quit()
    return print('ended')

def returnSum(myDict): 
    sum = 0
    for i in myDict: 
        sum = sum + myDict[i] 
    return sum

def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '') .replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url

    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    # print("final viewtimes: ", url_viewtime)

    return jsonify({'message': 'success!'}), 200

@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

model = pickle.load(open('model.pkl','rb'))

# executor = Executor(app)

app.secret_key = "flash message"

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'fatigue'

# mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/directpredict',methods=['POST'])
def directpredict():
    return render_template('directPred.html')

@app.route('/chromepredict',methods=['POST'])
def chromepredict():
    return render_template('chromePred.html')

@app.route('/chromeextension',methods=['POST','GET'])
def chromeextension():
    global driver
    driver = start()
    if request.method == "POST":
        name=request.form['name']
        email= request.form['email']
        country = request.form['country']
        salary = request.form['salary']
        file1 = open('myfile.txt', 'w') 
        s = salary
        file1.write(str(s)) 
        file1.close() 
    return render_template('extentionrunning.html',name=name,email=email,country=country,salary=salary)


@app.route('/endchromeextension',methods=['POST'])
def endchromeextension():
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    global driver
    global url_viewtime
    print("-----timming-----")
    print(url_viewtime)
    print("-----timming-----")
    dict = url_viewtime
    time = int(returnSum(dict))
    time = round(time/60,2)
    file1 = open('myfile.txt', 'r') 
    salary = file1.read()
    print(salary) 
    print(type(salary))
    prediction = model.predict([[time,int(salary)]])
    print(prediction)
    end(driver)
    # return render_template('extensionstop.html')
    if prediction[0] == 1 :
        return render_template('extensionstop.html',pred="Click on advertises.",time=time,salary=salary)
    else:
        return render_template('extensionstop.html',pred="Not click on advertises.",time=time,salary=salary)

@app.route('/handle')
def handle():
    return render_template('handle.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['projectFilepath']
    print(projectpath)
    return render_template('result.html',print=projectpath)

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == "POST":
        name=request.form['name']
        email= request.form['email']
        country = request.form['country']
        time = int(request.form['time'])
        salary = int(request.form['salary'])
        prediction = model.predict([[time,salary]])
        if prediction[0] == 1 :
            return render_template('result.html',name = name,pred="Click on advertises.")
        else:
            return render_template('result.html',name = name,pred="Not click on advertises.")

app.run(host='0.0.0.0', port=5000)    



if __name__ == "__main__":
    app.run(debug=True)
