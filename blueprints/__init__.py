import json, os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_restful import Resource, Api
import json, logging
from logging.handlers import RotatingFileHandler
import datetime
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

############################
#           JWT            #
############################

app.config['JWT_SECRET_KEY'] = 'SFsieaaabjsdalkjdi32jdijd32657j'
app.config['JWT_ACCES_TOKEN_EXPIRES'] = datetime.timedelta(days = 1)

jwt = JWTManager(app)

###########################
#         Database        #
###########################

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:8hamdiranu9@portofolio.cbxmczjsc4sm.ap-southeast-1.rds.amazonaws.com:3306/portofolio_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:8hamdiranu9@portofolio.cbxmczjsc4sm.ap-southeast-1.rds.amazonaws.com:3306/portofolio'

except Exception as e:
    raise e    

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if not claims['isadmin']:
            return {'status': 'FORBIDDEN', 'message': 'admin Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
mirate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)


######################
#  Import Blueprint  #
######################

@app.after_request
def after_request(response):
    try :
        requestData = request.get_json()
    except Exception as e :
        requestData = request.args.to_dict()
    if response.status_code == 200 :
        app.logger.info("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )

    elif response.status_code == 501 :
        app.logger.error("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )

    else:
        app.logger.warning("REQUEST_LOG\t%s",json.dumps({
            'status_code':response.status_code,
            'method':request.method,
            'code':response.status,
            'uri':request.full_path,
            'request': request.args.to_dict(),
            'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

from blueprints.User.resource import bp_user
from blueprints.Item.resource import bp_item
from blueprints.Cart.resource import bp_cart
from blueprints.Payment.resource import bp_payment
from blueprints.Checkout.resource import bp_checkout
from blueprints.auth import bp_auth

app.register_blueprint(bp_user, url_prefix = '/user')
app.register_blueprint(bp_item, url_prefix = '/item')
app.register_blueprint(bp_auth, url_prefix = '/token')
app.register_blueprint(bp_cart, url_prefix = '/cart')
app.register_blueprint(bp_checkout, url_prefix = '/checkout')
app.register_blueprint(bp_payment, url_prefix = '/payment')

db.create_all()
