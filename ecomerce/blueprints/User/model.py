from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__= "User"
    id              = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username        = db.Column(db.String(30), unique = True, nullable = False)
    first_name      = db.Column(db.String(30), nullable = False)
    last_name       = db.Column(db.String(30), nullable = False)
    gender          = db.Column(db.String(30), nullable = False)
    date_of_birth   = db.Column(db.String(20), nullable = False)
    address         = db.Column(db.String(2000), nullable = False)
    city            = db.Column(db.String(30), nullable = False)
    zip_code        = db.Column(db.String(30), nullable = True)
    phone_number    = db.Column(db.String(30), nullable = False)
    password        = db.Column(db.String(300), nullable = False)
    email           = db.Column(db.String(300), nullable = False)
    created_at      = db.Column(db.DateTime, default = datetime.datetime.now())
    update_at       = db.Column(db.DateTime, onupdate = datetime.datetime.now())
    deleted         = db.Column(db.Boolean, default = False)

    response_fields = {
        'id'            : fields.Integer,
        'username'      : fields.String,
        'first_name'    : fields.String,
        'last_name'     : fields.String,
        'gender'        : fields.String,
        'date_of_birth' : fields.String,
        'address'       : fields.String,
        'city'          : fields.String,
        'zip_code'      : fields.String,
        'phone_number'  : fields.String,
        'password'      : fields.String,
        'email'         : fields.String,
        'created_at'    : fields.DateTime,
        'update_at'     : fields.DateTime
    }

    jwt_claims_fields = {
        'id'        : fields.Integer,
        'username'  : fields.String,

    }

    def __init__(self, username, first_name, last_name, gender, date_of_birth, address, city, zip_code, phone_number, password, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.phone_number = phone_number
        self.password = password
        self.email = email

    def __repr_(self):
        return '<User %r>' %self.id