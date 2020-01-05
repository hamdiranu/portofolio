from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *

from .model import Payments
from blueprints.Cart.model import Carts
from blueprints.Checkout.model import Checkouts

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
        

        # Mendefinisikan nilai yang diambil dari table lain
        checkout_id = qry_checkout.id
        # jumlah_barang = qry_checkout.jumlah_barang
        # total_harga = qry_checkout.total_harga

        # Membuat table payment
        payment = Payments(checkout_id, args['cardholder'], args['card_number'], args['security_code'],
                    args['expired_month'], args['expired_year'], args['status_cod'])
        db.session.add(payment)
        db.session.commit()

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