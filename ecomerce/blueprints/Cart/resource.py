from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *

from .model import Carts
from blueprints.Item.model import Items
from blueprints.Cart_detail.model import Cartdetails
from blueprints.User.model import Users

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints import db,app, admin_required

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)


################################################
#              USING RESTFUL-API               #  
################################################


class CartResource(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

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
        parser.add_argument('product_id', location = 'json', required = True)
        parser.add_argument('total_product', location = 'json', required = True)
        args = parser.parse_args()

        # Memperoleh harga product
        product = Items.query.get(int(args['product_id']))
        harga = product.price

        # Menghitung total harga satu jenis product
        sub_total = harga * int(args['total_product'])

        verify_jwt_in_request()
        claims = get_jwt_claims()

        qry_cart = Carts.query.filter_by(user_id = claims["id"]).filter_by(status = False).first()
        
        # Cek cart sudah terbentuk atau belum terbentuk
        if qry_cart == None:
            
            # Menambahkan Cart baru    
            cart = Carts(claims["id"], 0, 0, False)
            db.session.add(cart)
            db.session.commit()
            
            # Mengambil data pada tabel Cart & Item
            qry_cart = Carts.query.filter_by(user_id = claims["id"]).filter_by(status = False).first()
            qry_item = Items.query.filter_by(id = int(args["product_id"])).first()

            # Menambahkan cart_detail baru
            cart_detail = Cartdetails(qry_cart.id, int(args["product_id"]), qry_item.item_name,
                 qry_item.price, int(args["total_product"]),sub_total)
            db.session.add(cart_detail)
            db.session.commit()

            # Update jumlah barang & total harga pada tabel Cart
            qry_cart.total_item += int(args["total_product"])
            qry_cart.total_harga += sub_total
            db.session.commit()

            return marshal(cart_detail, Cartdetails.response_fields), 200,
            {'Content-Type' : 'application/json' }
        
        else :

            # Cek apakah product id sudah terdaftar pada cart atau belum
            qry_cart_detail = Cartdetails.query.filter_by(cart_id = qry_cart.id).filter_by(product_id = 
                                int(args["product_id"])).first()
            qry_item = Items.query.filter_by(id = int(args["product_id"])).first()

            if qry_cart_detail == None:
                cart_detail = Cartdetails(qry_cart.id, int(args["product_id"]), qry_item.item_name,
                 qry_item.price, int(args["total_product"]),sub_total)
                db.session.add(cart_detail)
                db.session.commit()

                # Update jumlah barang & total harga pada tabel Cart
                qry_cart.total_item += int(args["total_product"])
                qry_cart.total_harga += sub_total
                db.session.commit()

                return marshal(cart_detail, Cartdetails.response_fields), 200, {'Content-Type' :
                                'application/json' }

            else :

                # Mengupdate data jika produk id telah terdaftar
                qry_cart_detail.total_product += int(args["total_product"])
                qry_cart_detail.sub_total += sub_total
                db.session.commit()

                # Update jumlah barang & total harga pada tabel Cart
                qry_cart.total_item += int(args["total_product"])
                qry_cart.total_harga += sub_total
                db.session.commit()

                return marshal(qry_cart_detail, Cartdetails.response_fields), 200, {'Content-Type' :
                                'application/json' }
    
    @jwt_required
    @admin_required
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
    @admin_required
    def patch(self):
        return 'Not yet implement', 501

class CartList(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

    def __init__(self):
        pass
    
    @jwt_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('user_id', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ("total_item","total_harga"))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Carts.query

        if args['user_id'] is not None:
            qry = qry.filter_by(user_id = args['user_id'])

        if args['orderby'] is not None :
            if args['orderby'] == 'total_item':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Carts.total_item))
                else:
                    qry = qry.order_by(Carts.total_item)
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

class CartDetailList(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

    def __init__(self):
        pass
    
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('user_id', location = 'args')
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ("total_item","total_harga"))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Cartdetails.query

        if args['user_id'] is not None:
            qry = qry.filter_by(user_id = args['user_id'])

        if args['orderby'] is not None :
            if args['orderby'] == 'total_item':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Cartdetails.total_item))
                else:
                    qry = qry.order_by(Cartdetails.total_item)
            elif args['orderby'] == 'total_harga':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Cartdetails.total_harga))
                else:
                    qry = qry.order_by(Cartdetails.total_harga)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Cartdetails.response_fields))
        return rows, 200

api.add_resource(CartList, '', '/list')
api.add_resource(CartResource, '', '/<id>')
api.add_resource(CartDetailList, '', '/detail')