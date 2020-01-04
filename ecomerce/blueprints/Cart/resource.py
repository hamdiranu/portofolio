from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Carts
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, internal_required

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)


################################################
#              USING RESTFUL-API               #  
################################################


class CartResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        qry = Carts.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Carts.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location = 'json', required = True)
        parser.add_argument('total_harga', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()

        cart = Carts(args['user_id'], args['total_harga'], args['status'])
        db.session.add(cart)
        db.session.commit()

        app.logger.debug('DEBUG : %s', cart)

        return marshal(cart, Carts.response_fields), 200, {'Content-Type' : 'application/json' }
    
    @jwt_required
    @internal_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location = 'json', required = True)
        parser.add_argument('total_harga', location = 'json')
        parser.add_argument('status', location = 'json')
        args = parser.parse_args()

        qry = Carts.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.user_id = args['user_id']
        qry.total_harga = args['total_harga']
        qry.status = args['status']
        db.session.commit()

        return marshal(qry, Carts.response_fields), 200, {'Content-Type' : 'application/json' }

    @jwt_required
    @internal_required
    def delete(self,id):
        qry = Carts.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Hard Delete
        # db.session.delete(qry)
        # db.session.commit()

        # Soft Delete
        qry.deleted = True
        db.session.commit()
        return {'status':'Deleted'}, 200

    @jwt_required
    @internal_required
    def patch(self):
        return 'Not yet implement', 501

class CartList(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('status', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ("status","total_harga"))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Carts.query

        if args['status'] is not None:
            qry = qry.filter_by(writer = args['status'])

        if args['orderby'] is not None :
            if args['orderby'] == 'status':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Carts.status))
                else:
                    qry = qry.order_by(Carts.status)
            elif args['orderby'] == 'total_harga':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Carts.total_harga))
                else:
                    qry = qry.order_by(Carts.total_harga)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Carts.response_fields))
        return rows, 200

api.add_resource(CartList, '', '/list')
api.add_resource(CartResource, '', '/<id>')