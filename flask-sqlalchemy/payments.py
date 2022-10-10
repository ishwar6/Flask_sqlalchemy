from unicodedata import category
from models.models import *
from flask import Blueprint, Flask, redirect, render_template, request, make_response, json, jsonify
from models.schemas import *
from datetime import datetime
from sqlalchemy.sql import func

payments = Blueprint('payments', __name__)

#relationship test
@payments.route("/get_user_payment_method/payment_type/<UPaymentMethodId>")
def test_relationship(UPaymentMethodId):
    Data = {}
    user_payment_method = User_Payment_Method.query.filter_by(id = UPaymentMethodId).first()
    payment_type = user_payment_method.payment_type.name
    Data["payment_type"]=payment_type
    Data["Status"]="Payment type for payment method with id "+UPaymentMethodId+" retrieved Successfully!"
    r = make_response(Data, 200)
    r.headers["Content-Type"] = "text/json"
    return r
