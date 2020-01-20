from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *

from .model import Checkouts
from blueprints.Cart.model import Carts

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, admin_required

bp_checkout = Blueprint('checkout', __name__)
api = Api(bp_checkout)


################################################
#              USING RESTFUL-API               #  
################################################


class CheckoutResource(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def get(self, id):
        qry = Checkouts.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Checkouts.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('nama_penerima', location = 'json')
        parser.add_argument('alamat', location = 'json')
        parser.add_argument('kode_pos', location = 'json')
        parser.add_argument('nomor_telepon', location = 'json')
        parser.add_argument('metode_pengiriman', location = 'json')
        args = parser.parse_args()

        verify_jwt_in_request()
        claims = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id = claims["id"]).filter_by(status = False).first()
        qry_checkout = Checkouts.query.filter_by(cart_id = qry_cart.id).first()

        if qry_checkout == None:
            cart_id = qry_cart.id
            jumlah_barang = qry_cart.total_item
            total_harga = qry_cart.total_harga

            checkout = Checkouts(cart_id, args['nama_penerima'], args['alamat'], args['kode_pos'],
                        args['nomor_telepon'], args['metode_pengiriman'], jumlah_barang, total_harga)
            db.session.add(checkout)
            db.session.commit()

            app.logger.debug('DEBUG : %s', checkout)

            return marshal(checkout, Checkouts.response_fields), 200, {'Content-Type' : 
            'application/json' }

        else :
            qry_checkout.nama_penerima = args["nama_penerima"]
            qry_checkout.alamat = args["alamat"]
            qry_checkout.kode_pos = args["kode_pos"]
            qry_checkout.nomor_telepon = args["nomor_telepon"]
            qry_checkout.metode_pengiriman = args["metode_pengiriman"]
            qry_checkout.jumlah_barang = qry_cart.total_item
            qry_checkout.total_harga = qry_cart.total_harga
            db.session.commit()

            return marshal(qry_checkout, Checkouts.response_fields), 200, {'Content-Type' : 'application/json' }
    
    
    @jwt_required
    @admin_required
    def delete(self,id):
        qry = Checkouts.query.get(id)

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

class CheckoutList(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

    def __init__(self):
        pass
    
    @jwt_required
    @admin_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('cart_id', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('cart_id',"nama_penerima"))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Checkouts.query

        if args['cart_id'] is not None:
            qry = qry.filter_by(cart_id = args['cart_id'])

        if args['orderby'] is not None :
            if args['orderby'] == 'cart_id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Checkouts.cart_id))
                else:
                    qry = qry.order_by(Checkouts.cart_id)
            elif args['orderby'] == 'nama_penerima':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Checkouts.nama_penerima))
                else:
                    qry = qry.order_by(Checkouts.nama_penerima)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Checkouts.response_fields))
        return rows, 200

api.add_resource(CheckoutList, '', '/list')
api.add_resource(CheckoutResource, '', '/<id>')