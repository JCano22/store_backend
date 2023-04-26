from flask import Flask, request
import json
from config import db #imports db variable from config.py

app = Flask(__name__)

@app.get("/")
def home():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is another page"


##### API ENDPOINTS ######
##### JSON #####

def fix_id(obj):
    #fix the object to be json parsable
    obj["_id"] = str(obj["_id"])
    return obj


@app.get("/api/about")
def about():
    me = {"name": "Jorge Cano"}
    return json.dumps(me)

@app.get("/api/catalog")
def get_catalog():
    products = []
    cursor = db.products.find({})
    for prod in cursor:
        products.append(fix_id(prod))

    return json.dumps(products)

@app.post("/api/catalog")
def save_product():
    data = request.get_json()
    db.products.insert_one(data)
    print(data)
    return json.dumps(fix_id(data))


#get request on /api/total
#return the total value of your catalog (sum of all prices)
@app.get("/api/total")
def get_total_price():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

#get /api/products
#return the number of products in the catalog
@app.get("/api/products")
def num_products():
    ctr = 0
    cursor = db.products.find({})
    for prod in cursor:
        ctr += 1

    return json.dumps(ctr)

app.run(debug=True)
