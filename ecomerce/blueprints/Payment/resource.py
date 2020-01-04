from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *

from .model import Payments
from blueprints.Cart.model import Carts

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
        parser.add_argument('status_cod', location = 'json')
        args = parser.parse_args()

        verify_jwt_in_request()
        claims = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id = claims["id"]).filter_by(status = False).first()
        qry_payment = Payments.query.filter_by(cart_id = qry_cart.id).first()

        if qry_payment == None:
            cart_id = qry_cart.id
            jumlah_barang = qry_cart.total_item
            total_harga = qry_cart.total_harga

            payment = Payments(cart_id, args['cardholder'], args['card_number'], args['security_code'],
                        args['expired_month'], args['status_cod'], jumlah_barang, total_harga)
            db.session.add(payment)
            db.session.commit()

            app.logger.debug('DEBUG : %s', payment)

            return marshal(payment, Payments.response_fields), 200, {'Content-Type' : 
            'application/json' }

        else :
            qry_payment.cardholder = args["cardholder"]
            qry_payment.card_number = args["card_number"]
            qry_payment.security_code = args["security_code"]
            qry_payment.expired_month = args["expired_month"]
            qry_payment.status_cod = args["status_cod"]
            qry_payment.jumlah_barang = qry_cart.total_item
            qry_payment.total_harga = qry_cart.total_harga
            db.session.commit()

            return marshal(qry_payment, Payments.response_fields), 200, {'Content-Type' : 'application/json' }
    
    @jwt_required
    @admin_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', location = 'json', required = True)
        parser.add_argument('nama_penerima', location = 'json')
        parser.add_argument('alamat', location = 'json')
        parser.add_argument('kode_pos', location = 'json')
        parser.add_argument('nomor_telepon', location = 'json')
        parser.add_argument('metode_pengiriman', location = 'json')
        args = parser.parse_args()

        # Untuk mengambil nilai jumlah barang & total harga
        qry_cart = Carts.query.get(id)
        jumlah_barang = qry_cart.total_item
        total_harga = qry_cart.total_harga

        qry = Payments.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.cart_id = args['cart_id']
        qry.nama_penerima = args['nama_penerima']
        qry.alamat = args['alamat']
        qry.kode_pos = args['kode_pos']
        qry.nomor_telepon = args['nomor_telepon']
        qry.metode_pengiriman = args['metode_pengiriman']
        qry.jumlah_barang = jumlah_barang
        qry.total_harga = total_harga

        db.session.commit()

        return marshal(qry, Payments.response_fields), 200, {'Content-Type' : 'application/json' }

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
        parser.add_argument('user_id', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('user_id'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Payments.query

        if args['user_id'] is not None:
            qry = qry.filter_by(user_id = args['user_id'])

        if args['orderby'] is not None :
            if args['orderby'] == 'user_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Payments.user_id))
                else:
                    qry = qry.order_by(Payments.user_id)
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Payments.response_fields))
        return rows, 200

api.add_resource(PaymentList, '', '/list')
api.add_resource(PaymentResource, '', '/<id>')