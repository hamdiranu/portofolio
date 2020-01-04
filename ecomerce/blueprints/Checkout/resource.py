from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Checkouts
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, internal_required

bp_checkout = Blueprint('checkout', __name__)
api = Api(bp_checkout)


################################################
#              USING RESTFUL-API               #  
################################################


class CheckoutResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self, id):
        qry = Checkouts.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Checkouts.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', location = 'json', required = True)
        parser.add_argument('nama_penerima', location = 'json', required = True)
        parser.add_argument('alamat', location = 'json')
        parser.add_argument('kode_pos', location = 'json')
        parser.add_argument('nomor_telepon', location = 'json')
        parser.add_argument('metode_pengiriman', location = 'json')
        parser.add_argument('jumlah_barang', location = 'json')
        parser.add_argument('total_harga', location = 'json')
        args = parser.parse_args()

        checkout = Checkouts(args['cart_id'], args['nama_penerima'], args['alamat'], args['kode_pos'],
                    args['nomor_telepon'], args['metode_pengiriman'], args['jumlah_barang'],
                    args['total_harga'])
        db.session.add(checkout)
        db.session.commit()

        app.logger.debug('DEBUG : %s', checkout)

        return marshal(checkout, Checkouts.response_fields), 200, {'Content-Type' : 'application/json' }
    
    @jwt_required
    @internal_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('title', location = 'json', required = True)
        parser.add_argument('isbn', location = 'json', required = True)
        parser.add_argument('writer', location = 'json')
        args = parser.parse_args()

        qry = Checkouts.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.title = args['title']
        qry.isbn = args['isbn']
        qry.writer = args['writer']
        db.session.commit()

        return marshal(qry, Checkouts.response_fields), 200, {'Content-Type' : 'application/json' }

    @jwt_required
    @internal_required
    def delete(self,id):
        qry = Checkouts.query.get(id)

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

class CheckoutList(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('writer', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('writer'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Checkouts.query

        # qry = Checkouts.query.filter(Checkouts.title.like("%"+args['title']+"%"))

        if args['writer'] is not None:
            qry = qry.filter_by(writer = args['writer'])

        if args['orderby'] is not None :
            if args['orderby'] == 'writer':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Checkouts.writer))
                else:
                    qry = qry.order_by(Checkouts.writer)
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Checkouts.response_fields))
        return rows, 200

api.add_resource(CheckoutList, '', '/list')
api.add_resource(CheckoutResource, '', '/<id>')