from flask import Flask, request, session
from flask import render_template

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# dress name, dress price
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
    return render_template('home.html')

@app.route("/checkout")
def checkout():
    context = {
        'DRESS_DETAILS': DRESS_DETAILS
    }
    return render_template('checkout.html',**context)

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
