from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT

db = SQLAlchemy()


class Product_Category(db.Model):
    __tablename__ = 'product_categories'

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    desc              = db.Column(db.Text())

    def __repr__(self):
        return f'<ProductCategory:{self.id}>'
        

class Product_Inventory(db.Model):
    __tablename__ = "product_inventory"

    id                = db.Column(db.Integer, primary_key=True)
    quantity          = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<ProductInventory:{self.id}>'


class Discount(db.Model):
    __tablename__ = "discounts"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    desc              = db.Column(db.Text())
    discount_percent  = db.Column(db.DECIMAL(3,2), nullable=False)
    active            = db.Column(TINYINT, nullable=False)

class Product(db.Model):
    __tablename__ = "products"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)
    desc              = db.Column(db.Text())
    category_id       = db.Column(db.Integer, db.ForeignKey('product_categories.id'), nullable=False)
    inventory_id      = db.Column(db.Integer, db.ForeignKey('product_inventory.id'), nullable=False)
    price             = db.Column(db.DECIMAL(20,3), nullable=False)
    discount_id       = db.Column(db.Integer, db.ForeignKey('discounts.id'))
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product:{self.id}>'


class User(db.Model):
    __tablename__ = "users"

    id                = db.Column(db.Integer, primary_key=True)
    username          = db.Column(db.String(100), nullable=False, unique=True)
    password          = db.Column(db.String(100), nullable=False)
    first_name        = db.Column(db.String(100), nullable=False)
    last_name         = db.Column(db.String(100))
    mobile            = db.Column(db.String(20))
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f'<User:{self.id} {self.username}>'


class Payment_Provider(db.Model):
    __tablename__ = "payment_providers"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)


class Payment_Details(db.Model):
    __tablename__ = "payment_details"

    id                = db.Column(db.Integer, primary_key=True)
    amount            = db.Column(db.DECIMAL(20,3), nullable=False)
    provider_id       = db.Column(db.Integer, db.ForeignKey("payment_providers.id"), nullable=False)
    status            = db.Column(db.String(20))
    payment_method    = db.Column(db.Integer, db.ForeignKey("payment_types.id"), nullable=False)
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f'<PaymentDetails:{self.id} {self.amount} {self.status}>'



class Order_Details(db.Model):
    __tablename__ = "order_details"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total             = db.Column(db.DECIMAL(20,3), nullable=False)
    payment_id        = db.Column(db.Integer, db.ForeignKey('payment_details.id'), nullable=False)
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow) 

    def __repr__(self):
        return f'<OrderDetails:{self.id} {self.user_id}>'


class Order_Items(db.Model):
    __tablename__ = "order_items"

    id                = db.Column(db.Integer, primary_key=True)
    order_id          = db.Column(db.Integer, db.ForeignKey("order_details.id"), nullable=False)
    product_id        = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity          = db.Column(db.Integer, default=1, nullable=False)
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow) 


class Cart(db.Model):
    __tablename__ = "carts"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total             = db.Column(db.DECIMAL(20,3), nullable=False)
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Cart:{self.id} User: {self.user_id}>'


class cart_item(db.Model):
    __tablename__ = "cart_items"

    id                = db.Column(db.Integer, primary_key=True)
    cart_id           = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id        = db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    quantity          = db.Column(db.Integer,default=1, nullable=False)
    created_at        = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    modified_at       = db.Column(db.DateTime(), nullable=False, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Cart Item:{self.id} Cart: {self.cart_id}>'


class User_Address(db.Model):
    __tablename__ = "user_addresses"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_line1     = db.Column(db.String(200), nullable=False)
    address_line2     = db.Column(db.String(200))
    city              = db.Column(db.String(50))
    postal_code       = db.Column(db.String(10))
    country           = db.Column(db.String(100))
    telephone         = db.Column(db.String(20))
    mobile            = db.Column(db.String(20))

class Payment_Types(db.Model):
    __tablename__ = "payment_types"

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(100), nullable=False)


class User_Payment_Method(db.Model):
    __tablename__ = "user_payment_methods"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_type_id   = db.Column(db.Integer,db.ForeignKey("payment_types.id"), nullable=False)
    payment_type      = db.relationship("Payment_Types", lazy= True)
    account_no        = db.Column(db.String(100), nullable=False)
    expiry            = db.Column(db.DateTime(), nullable=False)







