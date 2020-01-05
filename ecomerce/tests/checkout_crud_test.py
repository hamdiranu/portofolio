import json
from . import client, create_token, reset_db
from blueprints.Checkout.model import Checkouts
from blueprints import db

class TestCheckoutCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_checkout_post(self, client):
        token = create_token(False)

        data = {
            "nama_penerima"		:"Bimon",
            "alamat"			:"jl.Simpang taman Agung nomor 17",
            "kode_pos"			:"65146",
            "nomor_telepon"		:"081275980982",
            "metode_pengiriman"	:"JNE"
        }

        res = client.post('/checkout', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
    # ======================================= GET ==================================== #
    
    def test_checkout_get_id_admin(self, client):
        token = create_token(True)
        res = client.get('/checkout/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_checkout_get_id_admin_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/checkout/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # ======================================= GET_All ==================================== #

    def test_checkout_get_all_admin_cart_id_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"cart_id",
            "sort":"desc"
        }

        res = client.get('/checkout',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_checkout_get_all_admin_cart_id_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"cart_id",
            "sort":"asc"
        }

        res = client.get('/checkout',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_checkout_get_all_admin_nama_penerima_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"nama_penerima",
            "sort":"desc"
        }

        res = client.get('/checkout',query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200

    def test_checkout_get_all_admin_nama_penerima_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "cart_id":1,
            "orderby":"nama_penerima",
            "sort":"asc"
        }

        res = client.get('/checkout',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200
        
    # ======================================= DELETE ==================================== #

    def test_checkout_delete_id_admin(self, client):
        token = create_token(True)
        res = client.delete('/checkout/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_checkout_delete_id_admin_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/checkout/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_checkout_patch_admin(self, client):
        token = create_token(True)
        res = client.patch('/checkout',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501

    def test_checkout_no_cart_post(self, client):
        token = create_token(False)

        qry = Checkouts.query.get(1)

        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        # Hard Delete
        db.session.delete(qry)
        db.session.commit()

        data = {
            "nama_penerima"		:"Bimon",
            "alamat"			:"jl.Simpang taman Agung nomor 17",
            "kode_pos"			:"65146",
            "nomor_telepon"		:"081275980982",
            "metode_pengiriman"	:"JNE"
        }

        res = client.post('/checkout', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        self.idPerson = res_json['id']