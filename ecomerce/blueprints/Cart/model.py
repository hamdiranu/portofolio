from blueprints import db
from flask_restful import fields
import datetime

class Carts(db.Model):
    __tablename__= "Cart"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id         = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False)
    status          = db.Column(db.Boolean, default = False)
    total_item      = db.Column(db.Integer, nullable = True, default = 0)
    total_harga     = db.Column(db.Integer, nullable = True, default = 0)
    created_at      = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at       = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted         = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'           : fields.Integer,
        'user_id'      : fields.Integer,
        'status'       : fields.Boolean,
        'total_item'   : fields.Integer,
        'total_harga'  : fields.Integer,
        'created_at'   : fields.DateTime,
        'updated_at'   : fields.DateTime,
        'deleted'      : fields.Boolean,
    }

    def __init__(self, user_id, status, total_item, total_harga):
        self.user_id = user_id
        self.status = status
        self.total_item = total_item
        self.total_harga = total_harga

    def __repr_(self):
        return '<Book %r>' %self.id