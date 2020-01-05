import json
from . import client, create_token, reset_db

class TestPaymentCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_payment_post(self, client):
        token = create_token(False)

        data = {
            "cardholder"	:"Hamdi Ranuharja",
            "card_number"	:"09238193819",
            "security_code"	:"21313",
            "expired_month"	:"04",
            "expired_year"	:"2080",
            "status_cod"	:False
        }

        res = client.post('/payment', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
        self.idPerson = res_json['id']

    # ======================================= GET ==================================== #

    def test_payment_get_id_admin(self, client):
        token = create_token(True)
        res = client.get('/payment/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_payment_get_id_admin_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/payment/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # # ======================================= GET_All ==================================== #

    def test_payment_get_all_admin_checkout_id_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "checkout_id":1,
            "orderby":"checkout_id",
            "sort":"desc"
        }

        res = client.get('/payment',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_payment_get_all_admin_checkout_id_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "checkout_id":1,
            "orderby":"checkout_id",
            "sort":"asc"
        }

        res = client.get('/payment',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    # ======================================= DELETE ==================================== #

    def test_payment_delete_id_admin(self, client):
        token = create_token(True)
        res = client.delete('/payment/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_payment_delete_id_admin_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/payment/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_payment_patch_admin(self, client):
        token = create_token(True)
        res = client.patch('/payment',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501