from blueprints import db
from flask_restful import fields
import datetime

class Payments(db.Model):
    __tablename__= "Payment"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    checkout_id     = db.Column(db.Integer, db.ForeignKey("Checkout.id"), nullable = False)
    cardholder      = db.Column(db.String(255), nullable = True)
    card_number     = db.Column(db.String(255), nullable = True)
    security_code   = db.Column(db.String(255), nullable = True)
    expired_month   = db.Column(db.String(255), nullable = True)
    expired_year    = db.Column(db.String(255), nullable = True)
    status_cod      = db.Column(db.Boolean, default = False)
    created_at      = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at       = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted         = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'                : fields.Integer,
        'checkout_id'       : fields.Integer,
        'cardholder'        : fields.String,
        'card_number'       : fields.String,
        'security_code'     : fields.String,
        'expired_month'     : fields.String,
        'expired_year'      : fields.String,
        'status_cod'        : fields.Boolean,
        'created_at'        : fields.DateTime,
        'updated_at'        : fields.DateTime,
        'deleted'           : fields.Boolean
    }

    def __init__(self, checkout_id, cardholder, card_number, security_code, expired_month, expired_year,
                status_cod):
        self.checkout_id = checkout_id
        self.cardholder = cardholder
        self.card_number = card_number
        self.security_code = security_code
        self.expired_month = expired_month
        self.expired_year = expired_year
        self.status_cod = status_cod

    def __repr_(self):
        return '<Payment %r>' %self.id