import json
from . import client, create_token, reset_db

class TestUserCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_user_post_internal(self, client):
        token = create_token(True)

        data = {
            "name":"hamdi3",
            "age":25,
            "sex":"male",
            "client_id":1
        }

        res = client.post('/user', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
        self.idPerson = res_json['id']

    def test_user_post_internal_invalid(self, client):
        token = create_token(True)

        data = {
            "name":"hamdi3",
            "age":"dualima",
            "sex":"male",
            "client_id":1
        }

        res = client.post('/user', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        

    def test_user_post_noninternal(self, client):
        token = create_token(False)

        data = {
            "name":"hamdi4",
            "age":25,
            "sex":"male",
            "client_id":1
        }

        res = client.post('/user', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 403
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])

    # ======================================= GET ==================================== #

    def test_user_get_id_internal(self, client):
        token = create_token(True)
        res = client.get('/user/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_id_internal_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/user/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # ======================================= GET_All ==================================== #

    def test_user_get_all_internal_age_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "sex":"male",
            "orderby":"age",
            "sort":"desc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_all_internal_sex_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "sex":"male",
            "orderby":"sex",
            "sort":"desc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200


    def test_user_get_all_internal_age_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "sex":"male",
            "orderby":"age",
            "sort":"asc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_all_internal_sex_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "sex":"male",
            "orderby":"sex",
            "sort":"asc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    # ======================================= PUT ==================================== #

    def test_user_put_internal(self, client):
        token = create_token(True)

        data = {
            "name":"hamdi6",
            "age":25,
            "sex":"male",
            "client_id":1
        }

        res = client.put('/user/1', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
        self.idPerson = res_json['id']

    def test_user_put_internal_id_notfound(self, client):
        token = create_token(True)

        data = {
            "name":"hamdi6",
            "age":25,
            "sex":"male",
            "client_id":1
        }

        res = client.put('/user/100', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_user_put_internal_invalid(self, client):
        token = create_token(True)

        data = {
            "name":"hamdi6",
            "age":"dualima",
            "sex":"male",
            "client_id":1
        }

        res = client.put('/user/1', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 400
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
    def test_user_put_noninternal(self, client):
        token = create_token(False)

        data = {
            "name":"hamdi4",
            "age":25,
            "sex":"male",
            "client_id":1
        }

        res = client.put('/user/1', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 403
        # assert res_json['client_secret'] == hashlib.md5(data['client_secret'])
        
    # ======================================= DELETE ==================================== #

    def test_user_delete_id_internal(self, client):
        token = create_token(True)
        res = client.delete('/user/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_delete_id_internal_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/user/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_user_patch_internal(self, client):
        token = create_token(True)
        res = client.patch('/user',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501