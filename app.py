from flask import Flask, request, session, redirect, jsonify
from flask import render_template
import requests
import sqlite3

import utilities

def init_db():
    CONNECTION = sqlite3.connect('debei.sql')
    return CONNECTION

def create_app():
    app = Flask(__name__, )
    app.secret_key = 'BAD_SECRET_KEY'
    return app

app = create_app()

# dress name, dress price
# TODO: very good usecase for dataclasses
DRESS_DETAILS = (
    ('dress-1', 100),
    ('dress-2', 200),
    ('dress-3', 300),
    ('dress-4', 200),
    ('dress-5', 300),
    ('dress-6', 500)
)

@app.route("/")
def home():
    # this is a good place to init things on the session
    session.clear()

    # do a test query here
    db = init_db()
    cur = db.cursor()
    res = cur.execute("SELECT * FROM Items")

    context = {
        'dresses': res.fetchall()
    }
    
    return render_template('home.html',**context)

@app.route("/checkout")
def checkout():
    context = {
        'DRESS_DETAILS': DRESS_DETAILS,
        'utilities': utilities
    }
    return render_template('checkout.html',**context)

@app.route('/yoco_webhook', methods=['POST'])
def webhook():
    request_body = request.get_data(as_text=True)

    print(request_body)

    return "", 200

@app.route("/yoco_checkout", methods=['POST'])
def yoco_checkout():
    name = request.json['name'] # use on my side
    email = request.json['email'] # use on my side
    amount = request.json['total']

    url = "https://payments.yoco.com/api/checkouts"

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_test_26ec4ed84BgRWeWb5ce4e678d277'
    }

    body = {
        "amount": amount*100,
        "currency": "ZAR"
    }

    r = requests.post(url, headers=header, json=body)
    print(r.json()) # this is the response body :)
    rurl = r.json()['redirectUrl']

    response = jsonify({'redirect_url': rurl})
    response.headers.add('Content-Type', 'application/json')
    return response

@app.route("/add_to_cart/", methods=['POST'])
def add_to_cart():
    size = request.json['size']
    id = request.json['id']
    index = 0

    if not size in ('S','M','L'):
        print('unknown size')
        return ('none')
    
    for i in range(len(DRESS_DETAILS)):
        dress = DRESS_DETAILS[i]
        if dress[0] == id:
            index = i
            break
    else:        
        return ('none') # did not find id in DRESS_DETAILS

    if 'orders' in session:
        curr = session['orders'].copy() # performance be damned
        curr.append((size,index))
        session['orders'] = curr
    else:
        session['orders'] = [(size,index)]

    print(f"ORDERS = {session}")
    return ('none')
