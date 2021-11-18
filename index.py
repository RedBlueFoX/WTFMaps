from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import json
counter = 0
output = []
app = Flask(__name__)


@app.route("/")
def hello_world():
    url_for('static', filename='index.css')
    return render_template("index.html")

@app.route('/handle_data', methods=['POST', 'GET'])
def handle_data():
    global counter 
    global output
    f = open("static/questions.json",)
    data = json.load(f, strict = False)
    url_for('static', filename='Survey_template.css')
    if(counter == 6):
        print(output)
    if(request.method == 'GET'):
        counter = 0
    if(request.method == 'POST'):
        returndata = request.form['rate']
        output.append(returndata)
        counter = counter + 1
    return render_template("Survey_template.html", text = data['questions'][counter]['question'])