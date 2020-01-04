from blueprints import db
from flask_restful import fields
import datetime

class Checkouts(db.Model):
    __tablename__= "Checkout"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    cart_id         = db.Column(db.Integer, db.ForeignKey("Cart.id"), nullable = False)
    nama_penerima   = db.Column(db.String(255), nullable = False)
    alamat          = db.Column(db.String(255), nullable = False)
    kode_pos        = db.Column(db.String(255), nullable = False)
    nomor_telepon   = db.Column(db.String(255), nullable = False)
    metode_pengiriman = db.Column(db.String(255), nullable = False)
    jumlah_barang   = db.Column(db.Integer, nullable = True, default = 0)
    total_harga     = db.Column(db.Integer, nullable = True, default = 0)
    created_at      = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at       = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted         = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'                : fields.Integer,
        'cart_id'           : fields.Integer,
        'nama_penerima'     : fields.String,
        'alamat'            : fields.String,
        'kode_pos'          : fields.String,
        'nomor_telepon'     : fields.String,
        'metode_pengiriman' : fields.String,
        'jumlah_barang'     : fields.Integer,
        'total_harga'       : fields.Integer,
        'created_at'        : fields.DateTime,
        'updated_at'        : fields.DateTime,
        'deleted'           : fields.Boolean,
    }

    def __init__(self, cart_id, nama_penerima, alamat, kode_pos, nomor_telepon, metode_pengiriman,
                jumlah_barang,total_harga):
        self.cart_id = cart_id
        self.nama_penerima = nama_penerima
        self.alamat = alamat
        self.kode_pos = kode_pos
        self.nomor_telepon = nomor_telepon
        self.metode_pengiriman = metode_pengiriman
        self.jumlah_barang = jumlah_barang
        self.total_harga = total_harga

    def __repr_(self):
        return '<Book %r>' %self.id