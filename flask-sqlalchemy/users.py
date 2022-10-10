from models.models import *
from flask import Blueprint, Flask, redirect, render_template, request, make_response, json, jsonify
from models.schemas import *

users = Blueprint('users', __name__)


@users.route('/user/cart/<user_id>')
def get_user_cart(user_id):
    data ={}
    #get products in cart with details like quatity total cart price
    Cart_Products = db.session.query(Cart, cart_item, Product).join(cart_item, cart_item.cart_id==Cart.id).join(Product, cart_item.product_id==Product.id).filter(Cart.user_id==user_id).all()
    cart_schema = CartSchema()
    cart_item_schema = CartItemSchema()
    product_schema = ProductSchema()

    def Map(name1, Dict, ExtDict):
        for i in Dict:
            ExtDict[name1+i]=Dict[i]

    CP = []
    for Data in Cart_Products:
        response = {}
        cart = cart_schema.dump(Data[0])
        product = product_schema.dump(Data[2])
        cartitem = cart_item_schema.dump(Data[1])
        Map("cart_item", cartitem, response)
        Map("cart_",cart,response)
        Map("product_",product, response)
        CP.append(response)

    data["Cart_Products"]=CP
    r = make_response(data, 200)
    r.headers["Content-Type"] = "text/json"
    return r
    

