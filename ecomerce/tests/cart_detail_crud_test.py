import json
from . import client, create_token, reset_db
from blueprints.Cart.model import Carts
from blueprints.Checkout.model import Checkouts
from blueprints import db

class TestCartCrud():

    idPerson = 0
    reset_db()
    
    # ======================================= GET_All ==================================== #

    def test_cart_detail_get_all_admin_sub_total_desc(self, client):
        token = create_token(False)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"sub_total",
            "sort":"desc"
        }

        res = client.get('/cart/detail',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_detail_get_all_admin_sub_total_asc(self, client):
        token = create_token(False)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"sub_total",
            "sort":"asc"
        }

        res = client.get('/cart/detail',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_get_all_admin_total_product_desc(self, client):
        token = create_token(False)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"total_product",
            "sort":"desc"
        }

        res = client.get('/cart/detail',query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200

    def test_cart_get_all_admin_total_product_asc(self, client):
        token = create_token(False)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"total_product",
            "sort":"asc"
        }

        res = client.get('/cart/detail',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200
        

