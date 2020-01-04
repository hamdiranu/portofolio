from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Items
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, admin_required

bp_item = Blueprint('item', __name__)
api = Api(bp_item)


################################################
#              USING RESTFUL-API               #  
################################################


class ItemResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        qry = Items.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Items.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    @jwt_required
    @admin_required
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('item_name', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('kategori', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        parser.add_argument('spesifikasi_1', location = 'json', required = True)
        parser.add_argument('spesifikasi_2', location = 'json')
        parser.add_argument('spesifikasi_3', location = 'json')
        parser.add_argument('gambar_1', location = 'json', required = True)
        parser.add_argument('gambar_2', location = 'json')
        parser.add_argument('gambar_3', location = 'json')
        parser.add_argument('gambar_4', location = 'json')
        args = parser.parse_args()

        item = Items(args['item_name'], args['price'], args['kategori'], args['deskripsi'],
        args['spesifikasi_1'], args['spesifikasi_2'], args['spesifikasi_3'], args['gambar_1'],
        args['gambar_2'], args['gambar_3'], args['gambar_4'])
        db.session.add(item)
        db.session.commit()

        app.logger.debug('DEBUG : %s', item)

        return marshal(item, Items.response_fields), 200, {'Content-Type' : 'application/json' }
    
    @jwt_required
    @admin_required
    def put(self, id):

        parser = reqparse.RequestParser()
        parser.add_argument('item_name', location = 'json', required = True)
        parser.add_argument('price', location = 'json', required = True)
        parser.add_argument('kategori', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        parser.add_argument('spesifikasi_1', location = 'json', required = True)
        parser.add_argument('spesifikasi_2', location = 'json')
        parser.add_argument('spesifikasi_3', location = 'json')
        parser.add_argument('gambar_1', location = 'json', required = True)
        parser.add_argument('gambar_2', location = 'json')
        parser.add_argument('gambar_3', location = 'json')
        parser.add_argument('gambar_4', location = 'json')
        args = parser.parse_args()

        qry = Items.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.item_name = args['item_name']
        qry.price = args['price']
        qry.kategori = args['kategori']
        qry.deskripsi = args['deskripsi']
        qry.spesifikasi_1 = args['spesifikasi_1']
        qry.spesifikasi_2 = args['spesifikasi_2']
        qry.spesifikasi_3 = args['spesifikasi_3']
        qry.gambar_1 = args['gambar_1']
        qry.gambar_2 = args['gambar_2']
        qry.gambar_3 = args['gambar_3']
        qry.gambar_4 = args['gambar_4']
        db.session.commit()

        return marshal(qry, Items.response_fields), 200, {'Content-Type' : 'application/json' }

    @jwt_required
    @admin_required
    def delete(self,id):
        qry = Items.query.get(id)

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
    @admin_required
    def patch(self):
        return 'Not yet implement', 501

class ItemList(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('item_name', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('item_name','price'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Items.query

        # Pencarian item berdasarkan nama
        if args['item_name'] is not None:
            qry = qry.filter_by(item_name = args['item_name'])

        # Pengurutan item berdasarkan nama/harga
        if args['orderby'] is not None :
            if args['orderby'] == 'item_name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Items.item_name))
                else:
                    qry = qry.order_by(Items.item_name)
            elif args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Items.price))
                else:
                    qry = qry.order_by(Items.price)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Items.response_fields))
        return rows, 200

api.add_resource(ItemList, '', '/list')
api.add_resource(ItemResource, '', '/<id>')