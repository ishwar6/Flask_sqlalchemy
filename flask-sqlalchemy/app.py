from flask import Flask, request, make_response
from flask_cors import CORS
from models.models import *
from dotenv import load_dotenv
from flask_migrate import Migrate

import os

app = Flask(__name__)
CORS(app=app, origins=["*"])
BASELINK = os.getenv('BASELINK')
env_path = os.path.join(app.root_path, '.env')
load_dotenv(env_path)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db_host=os.getenv('DATABASE_HOST')
db_username=os.getenv('DATABASE_USERNAME')
db_password=os.getenv('DATABASE_PASSWORD')
db_name=os.getenv('DATABASE_NAME')


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app

migrate = Migrate(app, db)

from users import users
from products import products
from payments import payments

app.register_blueprint(payments)
app.register_blueprint(users)
app.register_blueprint(products)


@app.route("/")
def Index():
    return """Hello!
    <ul>
    <li> <a href='/user/cart/2'>Get User cart of user id 2</a></li>
    <li><a href='/products_of_category/1'>get Products of category 1</a></li>
    <li>Post Create Product using api at /new_product/ (look for conditions in code)</li>
    <li><a href='/get_products_count_group_by_category/'>Get Product count for every category</a></li>
    <li><a href='/get_products_with_conditional_inventory_qty'>Get products applied condition or_(quantity > 25,  quantity < 10)</a></li>
    <li><a href='/get_user_payment_method/payment_type/1'>Get payment type of a payment method of user with id 1</a></li>
    </ul>
    """


if __name__ == "__main__":
    app.run()