from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from blueprints.User.model import Users

import hashlib

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

# Resource

class CreateTokenResource(Resource):

    def options(self, id=None):
        return {'status':'ok'},200

    def post(self):
        # Create token

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        args = parser.parse_args()
        
        password = hashlib.md5(args['password'].encode()).hexdigest()

        if args['username'] == 'admin' and args['password'] == 'thisisadmin':
            token= create_access_token(identity = args['username'], user_claims = {'isadmin':True})
            return {'token':token}, 200

        else :
            qry = Users.query.filter_by(username = args['username']).filter_by(password = password)
            clientData = qry.first()

            if clientData is not None:
                clientData = marshal(clientData, Users.jwt_claims_fields)
                clientData['isadmin'] = False
                token= create_access_token(identity = args['username'], user_claims = clientData)
                return {'token':token,'id':clientData["id"]}, 200
            else:
                return {'status':'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401


api.add_resource(CreateTokenResource, '')
    