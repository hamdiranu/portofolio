from mailjet_rest import Client
import os

from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *

from .model import Payments
from blueprints.Cart.model import Carts
from blueprints.Cart_detail.model import Cartdetails
from blueprints.Checkout.model import Checkouts
from blueprints.User.model import Users

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, admin_required

bp_payment = Blueprint('payment', __name__)
api = Api(bp_payment)


################################################
#              USING RESTFUL-API               #  
################################################

class PaymentResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def get(self, id):
        qry = Payments.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Payments.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('cardholder', location = 'json')
        parser.add_argument('card_number', location = 'json')
        parser.add_argument('security_code', location = 'json')
        parser.add_argument('expired_month', location = 'json')
        parser.add_argument('expired_year', location = 'json')
        parser.add_argument('status_cod', type=inputs.boolean, location = 'json')
        args = parser.parse_args()

        verify_jwt_in_request()
        claims = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id = claims["id"]).filter_by(status = False).first()
        qry_checkout = Checkouts.query.filter_by(cart_id = qry_cart.id).first()
        qry_user = Users.query.filter_by(id = claims["id"]).first()
        
        # Mendefinisikan nilai yang diambil dari table lain
        checkout_id = qry_checkout.id
        jumlah_barang = qry_checkout.jumlah_barang
        total_harga = qry_checkout.total_harga


        # Membuat table payment
        payment = Payments(checkout_id, args['cardholder'], args['card_number'], args['security_code'],
                    args['expired_month'], args['expired_year'], args['status_cod'])
        db.session.add(payment)
        db.session.commit()

        # Membuat API untuk pengiriman email detail pembelian
        api_key = '618175b9863eb14b6dab6e4abac8c57e'
        api_secret = '5442e1b5de0a695f518e9041af818e94'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Isi Email
        email_ecomerce = 'https://www.e-comerce.com/'
        gratitute = "<h3>Dear Costumer, </h3>"
        list_item_pembuka = "Berikut list barang yang telah dibeli :<br /><ol>"
        # Menambahkan list barang pada isi email
        qry_cart_details = Cartdetails.query.filter_by(cart_id = qry_cart.id)
        for item in qry_cart_details:
            list_item_pembuka += "{} ,<br/>Harga : {} ,<br/>dengan jumlah barang : {}<br/><br/>".format(
                item.product_name, item.product_price, item.total_product)
        total_barang = "<br />Jumlah Barang = {}".format(jumlah_barang)
        info_total = "<br />Total Belanja = Rp {}<br />".format(total_harga)
        kalimat_penutup = "<br />Thank you for purchasing items from <a href="+email_ecomerce+">e-comerce</a>!<br />May the delivery force be with you!"

        data = {
        'Messages': [
            {
            "From": {
                "Email": "hamdi@alterra.id",
                "Name": "Admin"
            },
            "To": [
                {
                "Email": "{}".format(qry_user.email),
                "Name": "{} {}".format(qry_user.first_name, qry_user.last_name)
                }
            ],
            "Subject": "Payment Confirmation",
            "TextPart": "My first Mailjet email",
            "HTMLPart": gratitute+list_item_pembuka+"<ol/>"+total_barang+info_total+kalimat_penutup,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)

        qry_cart.status = True
        db.session.commit()

        app.logger.debug('DEBUG : %s', payment)

        return marshal(payment, Payments.response_fields), 200, {'Content-Type' : 
        'application/json' }

    @jwt_required
    @admin_required
    def delete(self,id):
        qry = Payments.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Soft Delete
        qry.deleted = True
        db.session.commit()
        return {'status':'Deleted'}, 200

    @jwt_required
    @admin_required
    def patch(self):
        return 'Not yet implement', 501

class PaymentList(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @admin_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('checkout_id', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('checkout_id'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Payments.query

        if args['checkout_id'] is not None:
            qry = qry.filter_by(checkout_id = args['checkout_id'])

        if args['orderby'] is not None :
            if args['orderby'] == 'checkout_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Payments.checkout_id))
                else:
                    qry = qry.order_by(Payments.checkout_id)
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Payments.response_fields))
        return rows, 200

api.add_resource(PaymentList, '', '/list')
api.add_resource(PaymentResource, '', '/<id>')