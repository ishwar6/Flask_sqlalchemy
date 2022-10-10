from pyexpat import model
from xml.etree.ElementInclude import include
import app
from flask_marshmallow import Marshmallow
from .models import *
from marshmallow import Schema, fields
from sqlalchemy import func

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        include_fk = True


class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = cart_item
        include_fk = True
