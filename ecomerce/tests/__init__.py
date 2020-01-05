import pytest, json, logging
from blueprints import app, db
from app import cache
from flask import Flask, request

from blueprints.User.model import Users
from blueprints.Cart.model import Carts
from blueprints.Checkout.model import Checkouts
from blueprints.Item.model import Items

def reset_db():
    db.drop_all()
    db.create_all()

    # Menginput 1 data (initial value) user ke tabel
    data_user = Users("username01", "Hamdi", "Ranuharja", "Male", "09 April 2000",
    "jl.Simpang taman Agung nomor 17", "Malang", "65146", "081275980982",
    "2222b0104b5621b7a68474f2741bcbf1", "hamdi@alterra.id")
    db.session.add(data_user)
    db.session.commit()

    # Menginput 1 data (initial value) Cart ke tabel
    data_cart = Carts(1, False, 4, 5000000)
    db.session.add(data_cart)
    db.session.commit()

    # Menginput 1 data (initial value) Checkout ke tabel
    data_checkout = Checkouts(1, "Bimon", "jl.Simpang taman Agung nomor 17", "65146", "081275980982", "JNE", 7, 5000000)
    db.session.add(data_checkout)
    db.session.commit()

    # Menginput 1 data (initial value) item ke tabel
    data_item = Items("Jaket Hitam, S", 195000, "FA", "RE", "sp1", "sp2", "sp3", "ht", "ht", "ht", "ht")
    db.session.add(data_item)
    db.session.commit()

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isadmin=False):
    if isadmin:
        cachename = 'test-admin-token'
        data = {
            "username":"admin",
            "password":"thisisadmin"
        }
    else:
        cachename = 'test-token'
        data = {
            "username":"username01",
            "password":"username1"
        }

    token = cache.get(cachename)

    if token is None:
        # Do request
        req = call_client(request)
        res = req.get('/token',query_string = data)

        # Store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        # assert / compare with expected result
        assert res.status_code == 200

        # save token into cache
        cache.set(cachename, res_json['token'], timeout = 60)

        # return, because it usefull for other test
        return res_json['token']
    
    else:
        return token

