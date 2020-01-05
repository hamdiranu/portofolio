from blueprints import db
from flask_restful import fields
import datetime

class Cartdetails(db.Model):
    __tablename__= "Cartdetail"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cart_id         = db.Column(db.Integer, db.ForeignKey("Cart.id"), nullable = False)
    product_id      = db.Column(db.Integer, db.ForeignKey("Item.id"), nullable = False)
    product_name    = db.Column(db.String(255), nullable = True)
    product_price   = db.Column(db.Integer, nullable = True)
    total_product   = db.Column(db.Integer, nullable = True, default = 0)
    sub_total       = db.Column(db.Integer, nullable = True, default = 0)
    created_at      = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at       = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted         = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'           : fields.Integer,
        'cart_id'      : fields.Integer,
        'product_id'   : fields.Integer,
        'product_name' : fields.String,
        'product_price': fields.Integer,
        'total_product': fields.Integer,
        'sub_total'    : fields.Integer,
        'created_at'   : fields.DateTime,
        'updated_at'   : fields.DateTime,
        'deleted'      : fields.Boolean
    }

    def __init__(self, cart_id, product_id, product_name, product_price, total_product, sub_total):
        self.cart_id = cart_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.total_product = total_product
        self.sub_total = sub_total

    def __repr_(self):
        return '<Cartdetail %r>' %self.id