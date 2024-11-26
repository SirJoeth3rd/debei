from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/add_to_cart/", methods=['POST'])
def add_to_cart():
    print(request.json['size'])
    return ('none')
