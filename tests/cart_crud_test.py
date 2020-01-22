import json
from . import client, create_token, reset_db
from blueprints.Cart.model import Carts
from blueprints.Checkout.model import Checkouts
from blueprints import db

class TestCartCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_cart_post(self, client):
        token = create_token(False)

        data = {
                "product_id":"1",
                "total_product":"1"
            }

        res = client.post('/cart', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0


    def test_cart_sudahada_post(self, client):
        token = create_token(False)

        data = {
                "product_id":"1",
                "total_product":"1"
            }

        res = client.post('/cart', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0

        
    # ======================================= GET ==================================== #
    
    def test_cart_get_id_admin(self, client):
        token = create_token(True)
        res = client.get('/cart/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_get_id_admin_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/cart/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # ======================================= GET_All ==================================== #

    def test_cart_get_all_admin_total_harga_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "user_id":1,
            "orderby":"total_harga",
            "sort":"desc"
        }

        res = client.get('/cart',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_get_all_admin_total_harga_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "user_id":1,
            "orderby":"total_harga",
            "sort":"asc"
        }

        res = client.get('/cart',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_get_all_admin_total_item_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "user_id":1,
            "orderby":"total_item",
            "sort":"desc"
        }

        res = client.get('/cart',query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200

    def test_checkout_get_all_admin_total_item_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "user_id":1,
            "orderby":"total_item",
            "sort":"asc"
        }

        res = client.get('/cart',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200
        
    # ======================================= DELETE ==================================== #

    def test_cart_delete_id_admin(self, client):
        token = create_token(True)
        res = client.delete('/cart/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_cart_delete_id_admin_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/cart/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_cart_patch_admin(self, client):
        token = create_token(True)
        res = client.patch('/cart',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501

