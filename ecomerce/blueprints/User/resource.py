from flask import Blueprint
from flask_restful import Api, reqparse, marshal, Resource, inputs
from sqlalchemy import desc
from . import *
from .model import Users
import hashlib,datetime

from blueprints import db,app, admin_required
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims, jwt_required
from blueprints.User.model import Users

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

# Password Encription
from password_strength import PasswordPolicy

################################################
#              USING RESTFUL-API               #  
################################################


class UserResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @admin_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None and qry.deleted == False:
            return marshal(qry, Users.response_fields), 200
        return {'status':'NOT_FOUND'}, 404

    def post(self):

        policy = PasswordPolicy.from_names(
            length = 6
            # uppercase = 2,
            # numbers = 1,
            # special = 2
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('first_name', location = 'json', required = True)
        parser.add_argument('last_name', location = 'json')
        parser.add_argument('gender', location = 'json')
        parser.add_argument('date_of_birth', location = 'json')
        parser.add_argument('address', location = 'json')
        parser.add_argument('city', location = 'json')
        parser.add_argument('zip_code', location = 'json')
        parser.add_argument('phone_number', location = 'json')
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            user = Users(args['username'], args['first_name'], args['last_name'],
                args['gender'],args['date_of_birth'],args['address'],args['city'],
                args['zip_code'],args['phone_number'],password_digest,args['email'])
            db.session.add(user)
            db.session.commit()

            app.logger.debug('DEBUG : %s', user)
            return marshal(user, Users.response_fields), 200, {'Content-Type' : 'application/json' }
            
    @jwt_required
    def put(self, id):

        policy = PasswordPolicy.from_names(
            length = 6,
            # uppercase = 2,
            # numbers = 1,
            # special = 2
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json')
        parser.add_argument('first_name', location = 'json')
        parser.add_argument('last_name', location = 'json')
        parser.add_argument('gender', location = 'json')
        parser.add_argument('date_of_birth', location = 'json')
        parser.add_argument('address', location = 'json')
        parser.add_argument('city', location = 'json')
        parser.add_argument('zip_code', location = 'json')
        parser.add_argument('phone_number', location = 'json')
        parser.add_argument('password', location = 'json')
        parser.add_argument('email', location = 'json')
        args = parser.parse_args()

        qry = Users.query.get(id)

        validation = policy.test(args['password'])
        password_digest = ''
        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()


        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
      
        qry.username = args['username']
        qry.first_name = args['first_name']
        qry.last_name = args['last_name']
        qry.gender = args['gender']
        qry.date_of_birth = args['date_of_birth']
        qry.city = args['city']
        qry.zip_code = args['zip_code']
        qry.phone_number = args['phone_number']
        qry.password = password_digest
        qry.email = args['email']

        db.session.commit()

        return marshal(qry, Users.response_fields), 200, {'Content-Type' : 'application/json' }

    @jwt_required
    @admin_required
    def delete(self,id):
        qry = Users.query.get(id)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Hard Delete
        # db.session.delete(qry)
        # db.session.commit()

        # Soft Delete
        qry.deleted = True
        db.session.commit()
        return {'status':'Deleted'}, 200

    # @jwt_required
    # @admin_required
    def patch(self):
        return 'Not yet implement', 501

class UserList(Resource):

    def __init__(self):
        pass

    # @jwt_required
    # @admin_required
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('p', location = 'args', type = int, default = 1)
        parser.add_argument('rp', location = 'args', type = int, default = 25)
        parser.add_argument('gender', location = 'args', help = 'invalid sort value', choices = ('Male','Female','Others'))
        parser.add_argument('orderby', location = 'args', help = 'invalid sort value', choices = ('gender','username'))
        parser.add_argument('sort', location = 'args', help = 'invalid sort value', choices = ('desc','asc'))
        
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Users.query

        if args['gender'] is not None:
            qry = qry.filter_by(gender = args['gender'])

        if args['orderby'] is not None :
            if args['orderby'] == 'gender':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.gender))
                else:
                    qry = qry.order_by(Users.gender)
            elif args['orderby'] == 'username':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.username))
                else:
                    qry = qry.order_by(Users.username)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            if row is not None and row.deleted == False:
                rows.append(marshal(row,Users.response_fields))
        return rows, 200

api.add_resource(UserList, '', '/list')
api.add_resource(UserResource, '', '/<id>')
