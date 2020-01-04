from blueprints import db
from flask_restful import fields
import datetime

class Items(db.Model):
    __tablename__= "Item"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    item_name       = db.Column(db.String(255), unique = True, nullable = False)
    price           = db.Column(db.Integer, nullable = True)
    kategori        = db.Column(db.String(50), nullable = True)
    deskripsi       = db.Column(db.Text, nullable = False)
    spesifikasi_1   = db.Column(db.String(255), nullable = False)
    spesifikasi_2   = db.Column(db.String(255), nullable = False)
    spesifikasi_3   = db.Column(db.String(255), nullable = False)
    gambar_1        = db.Column(db.String(255), nullable = False)
    gambar_2        = db.Column(db.String(255), nullable = False)
    gambar_3        = db.Column(db.String(255), nullable = False)
    gambar_4        = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'           : fields.Integer,
        'item_name'    : fields.String,
        'price'        : fields.Integer,
        'kategori'     : fields.String,
        'deskripsi'    : fields.String,
        'spesifikasi_1': fields.String,
        'spesifikasi_2': fields.String,
        'spesifikasi_3': fields.String,
        'gambar_1'     : fields.String,
        'gambar_2'     : fields.String,
        'gambar_3'     : fields.String,
        'gambar_4'     : fields.String,
        'created_at'   : fields.DateTime,
        'updated_at'   : fields.DateTime,
        'deleted'      : fields.Boolean,
        
    }

    def __init__(self, item_name, price, kategori, deskripsi, spesifikasi_1, spesifikasi_2,
    spesifikasi_3, gambar_1, gambar_2, gambar_3, gambar_4):
        self.item_name = item_name
        self.price = price
        self.kategori = kategori
        self.deskripsi = deskripsi
        self.spesifikasi_1 = spesifikasi_1
        self.spesifikasi_2 = spesifikasi_2
        self.spesifikasi_3 = spesifikasi_3
        self.gambar_1 = gambar_1
        self.gambar_2 = gambar_2
        self.gambar_3 = gambar_3
        self.gambar_4 = gambar_4

    def __repr_(self):
        return '<Item %r>' %self.id