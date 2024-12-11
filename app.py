from flask import Flask, request, session, redirect, jsonify, url_for
from flask import render_template
import requests
import sqlite3
from contextlib import contextmanager
import jwt

import utilities

JWT_PASSWORD = "@pparently_a_very_d^b_sec5t_k55"

@contextmanager
def get_db():
    connection = sqlite3.connect('debei.db')
    yield connection.cursor()
    connection.commit()
    connection.close()

def create_app():
    app = Flask(__name__, )
    app.secret_key = 'BAD_SECRET_KEY'
    return app

app = create_app()

@app.route("/")
def home():
    # this is a good place to init things on the session
    session.clear()

    with get_db() as db:
        res = db.execute("select * from Items").fetchall()

    context = {
        'dresses': res
    }
    
    return render_template('home.html',**context)


@app.route("/checkout")
def checkout():
    context = {
        'utilities': utilities
    }
    return render_template('checkout.html',**context)

@app.route("/thank_you/<order_jwt>")
def thank_you(order_jwt):
    # TODO check if the payment was a success and set it on the order
    with get_db() as cur:
        query = "select * from Orders where order_nbr = ?"
        try:
            jwt_dict = jwt.decode(order_jwt, JWT_PASSWORD, ["HS256"])
            order_nbr = jwt_dict['order_nbr']
        except jwt.InvalidSignatureError:
            # some hacky stuff here
            return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        
        order = cur.execute(query, (order_nbr,)).fetchone()
        if order:
            print('Order placed succesfully!')
            query = "update Orders set status = 'matched' where order_nbr = ?"
            cur.execute(query, (order_nbr,))

            return "thank you your order has been placed"
    
    return "order failed to place, if this was unintentional please contact us"

@app.route("/yoco_checkout", methods=['POST'])
def yoco_checkout():
    name = request.json['name'] # use on my side
    email = request.json['email'] # use on my side
    order_items = session['orders']
    total = utilities.sum_dresses_price(order_items)

    with get_db() as cur:
        # create the order
        query = "insert into Orders (name, email) values (?,?)"
        print(f'ORDER QUERY VALUES: {(name, email)}')
        res = cur.execute(query, (name, email))
        order_nbr = res.lastrowid

        # now link the orders with the items
        query = "insert into OrderItems (item_nbr, order_nbr, item_size) values (?,?,?)"
        for item in order_items:
            cur.execute(query, (item[1], order_nbr, item[0]))

    url = "https://payments.yoco.com/api/checkouts"

    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk_test_26ec4ed84BgRWeWb5ce4e678d277'
    }

    order_jwt = jwt.encode({'order_nbr': order_nbr}, JWT_PASSWORD, algorithm="HS256")
    
    session['order'] = order_jwt

    body = {
        "amount": total,
        "currency": "ZAR",
        "successUrl": f"http://localhost:5000/thank_you/{order_jwt}", # TODO: add order-id as variable, remember to encrypt
        "metadata": {
            "order_nbr": order_nbr # don't have to encode this (I hope)
        }
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

    with get_db() as dbcur:
        query = "select * from Items where name=?"
        dress_info = dbcur.execute(query, (id,)).fetchone()

    if not size in ('S','M','L'):
        print('unknown size')
        return ('none')

    if 'orders' in session:
        curr = session['orders'].copy() # performance be damned
        curr.append((size,) + dress_info)
        session['orders'] = curr
    else:
        session['orders'] = [(size,) + dress_info]
        
    return ('none')
