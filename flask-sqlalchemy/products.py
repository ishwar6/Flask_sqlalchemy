from models.models import *
from flask import Blueprint, Flask, redirect, render_template, request, make_response, json, jsonify
from models.schemas import *
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import or_

products = Blueprint('products', __name__)


#simple select query
@products.route("/products_of_category/<cat_id>")
def get_product_by(cat_id):
    products = Product.query.filter_by(category_id=cat_id).all()
    product_schema = ProductSchema(many=True)
    products = product_schema.dump(products)
    Data = {}
    Data["products"] = products
    r = make_response(Data, 200)
    r.headers["Content-Type"] = "text/json"
    return r


@products.route("/new_product/", methods=["POST"])
def create_product():
    #check passed args
    keys = ["name","desc","category_id","price"]
    for key in keys:
        if key not in request.json:
            raise Exception("Key: "+key+" not Present in request")
    if "inventory_id" not in request.json:
        quantity = request.json["quantity"]
        if quantity == None:
            raise Exception("Key: Quantity not Present in request")
        inventory = Product_Inventory(quantity=quantity)
        db.session.add(inventory)
        db.session.commit()
        inventory_id = inventory.id
    else:
        inventory_id = request.json["inventory_id"]
    if "discount_id" not in request.json:
        discount_id = None
    else:
         discount_id = request.json["discount_id"]
    product = Product(
            name = request.json["name"],
            desc = request.json["desc"],
            category_id = request.json["category_id"],
            inventory_id = inventory_id,
            price = request.json["price"],
            discount_id = discount_id,
            created_at = datetime.now(),
            modified_at = datetime.now(),
        )
    db.session.add(product)
    db.session.commit()
    data = {}
    data["Status"] = "Successfully Product Added"
    r = make_response(data, 200)
    r.headers["Content-Type"] = "text/json"
    return r


@products.route("/get_products_count_group_by_category/")
def get_products_by_cats():
    try:
        query = db.session.query(func.count(Product.id).label("Product_count"),Product_Category.name).join(Product_Category, Product.category_id==Product_Category.id, isouter=True).group_by(Product_Category.id)
    except Exception as e:
        print(e)
    print(query)
    products = query.all()
    required = []
    for i in products:
        required.append(dict(i))
    data = {}
    data["Products_count_by_categories"] = required 
    data["Status"] = "Successfully Products' count by Category retrieved"
    r = make_response(data, 200)
    r.headers["Content-Type"] = "text/json"
    return r


@products.route("/get_products_with_conditional_inventory_qty")
def get_conditional_products():
    #random Condition for testing
    query = db.session.query(Product.id, Product.name, Product_Inventory.id, Product_Inventory.quantity).join(Product_Inventory, Product_Inventory.id==Product.inventory_id).filter(or_(Product_Inventory.quantity>25, Product_Inventory.quantity<10))
    required_data = query.all()
    required_data = [dict(i) for i in required_data]
    data = {}
    data["required_data"]=required_data
    data["Status"] = "Successfully used Or operator and satisfied condition for testing"
    r = make_response(data, 200)

    r.headers["Content-Type"] = "text/json"
    return r