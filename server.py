from flask import Flask, request, abort
import json
from config import db  # imports db variable from config.py
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # disable CORS security rule


@app.get("/")
def home():
    return "Hello from Flask"


@app.get("/test")
def test():
    return "This is another page"


##### API ENDPOINTS ######
##### JSON #####

def fix_id(obj):
    # fix the object to be json parsable
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

    # apply validation

    if "title" not in data or len(data["title"]) < 6:
        return abort(400, "Invalid Title")

    if "price" not in data:
        return abort(400, "Invalid Price")

    if not isinstance(data["price"], (int, float)):
        return abort(400, "Invalid Price")

    if data["price"] <= 0:
        return abort(400, "Invalid Price")

    # BR3: there must be a catalog
    if "catalog" not in data:
        return abort(400, "Invalid Category")

    db.products.insert_one(data)
    return json.dumps(fix_id(data))


@app.get("/api/catalog/byid/<id>")
def get_product_by_id(id):
    db_id = ObjectId(id)
    prod = db.products.find({"_id": db_id})
    if prod is None:
        return abort(404, "Product Not Found.")

    return json.dumps(fix_id(prod))


# get request on /api/total
# return the total value of your catalog (sum of all prices)
@app.get("/api/total")
def get_total_price():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

# get /api/products
# return the number of products in the catalog


@app.get("/api/products")
def num_products():
    ctr = 0
    cursor = db.products.find({})
    for prod in cursor:
        ctr += 1

    return json.dumps(ctr)


# get /api/categories
# should return the list of categories
# retrieve all products, get the category and put it on a list
# then return the list as json
@app.get("/api/categories")
def get_category():
    categories = []
    cursor = db.products.find({})
    for prod in cursor:
        cat = prod['category']
        if cat not in categories:
            categories.append(cat)

    return json.dumps(categories)


# declaring a variable in an endpoint
@app.get("/api/products/categories/<name>")
def get_by_category(name):
    results = []
    cursor = db.products.find({})
    for prod in cursor:
        if prod["category"] == name:
            results.append(fix_id(prod))
    return json.dumps(results)

# get /api/products/search/test


@app.get("/api/products/search/<term>")
def search_products(term):
    results = []
    cursor = db.products.find({"title": {"$regex": term, "$options": "i"}})
    for prod in cursor:
        results.append(fix_id(prod))
    return json.dumps(results)


# create a get end point on /api/products/lower/value
# to retrieve all products whose price is lower than given value
@app.get("/api/products/lower/<value>")
def price_lower(value):
    results = []
    value = float(value)
    cursor = db.products.find({"price": {"$lt": value}})
    for prod in cursor:
        results.append(fix_id(prod))
    return json.dumps(results)


# to retrieve all products whose price is greater than or equal to given value
@app.get("/api/products/greater/<value>")
def price_greater(value):
    results = []
    value = float(value)
    cursor = db.products.find({"price": {"$gte": value}})
    for prod in cursor:
        results.append(fix_id(prod))
    return json.dumps(results)


@app.delete("/api/catalog/<title>")
def del_by_prod(title):
    db.products.delete_one({"title": title})
    return json.dumps({"status": "OK", "message": "Product Deleted"})


@app.delete("/api/catalog/byid/<id>")
def delete_by_id(id):
    db_id = ObjectId(id)
    db.products.delete_one({"_id": db_id})
    return json.dumps({"status": "OK", "message": "Product Deleted"})


#################################
######### COUPON CODE###########

# GET /api/coupons - retrieve all
# POST /api/coupon - save new
# GET /api/coupon/<code> - search 1 by code
@app.get("/api/coupons")
def get_coupon():
    coupons = []
    cursor = db.coupons.find({})
    for coup in cursor:
        coupons.append(fix_id(coup))

    return json.dumps(coupons)


@app.post("/api/coupons")
def save_coupons():
    data = request.get_json()
    if "code" not in data or len(data["code"]) < 5:
        return abort(400, "Invalid Coupon")

    if "discount" not in data:
        return abort(400, "Invalid Coupon")

    if not isinstance(data["discount"], (int, float)):
        return abort(400, "Invalid Discount")

    if data["discount"] < 5 or data["discount"] > 40:
        return abort(400, "Invalid Discount")

    existing = db.coupons.find_one({"code": data["code"]})
    if existing:
        return abort(404, "Code already exists in coupon list.")

    db.coupons.insert_one(data)
    return json.dumps(fix_id(data))


@app.get("/api/coupons/<code>")
def get_by_code(code):
    coupon = db.coupons.find_one({"code": code})
    if not coupon:
        return abort(404, "Invalid Code")

    return json.dumps(fix_id(coupon))


@app.delete("/api/coupons/<code>")
def del_by_code(code):
    coupon = db.coupons.delete_one({"code": code})
    return json.dumps({"status": "OK", "message": "Coupon Deleted"})


# app.run(debug=True)
