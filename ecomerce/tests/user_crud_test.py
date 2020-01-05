import json
from . import client, create_token, reset_db

class TestUserCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_user_post_admin(self, client):
        token = create_token(True)

        data = {
                "username"		:"username3",
                "first_name"	:"leli",
                "last_name"		:"anto",
                "gender"		:"Female",
                "date_of_birth"	:"15 Oktober 1500",
                "address"		:"jl.Simpang taman Agung nomor 107",
                "city"			:"Malang",
                "zip_code"		:"65146",
                "phone_number"	:"081275988888",
                "password"		:"username3",
                "email"			:"lelianto@alterra.id"
            }

        res = client.post('/user', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
        self.idPerson = res_json['id']

    # ======================================= GET ==================================== #

    def test_user_get_id_admin(self, client):
        token = create_token(True)
        res = client.get('/user/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_id_admin_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/user/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # # ======================================= GET_All ==================================== #

    def test_user_get_all_admin_gender_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "gender":"Male",
            "orderby":"gender",
            "sort":"desc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_all_admin_username_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "gender":"Male",
            "orderby":"username",
            "sort":"desc"
        }

        res = client.get('/user',query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200


    def test_user_get_all_admin_username_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "gender":"Male",
            "orderby":"username",
            "sort":"asc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_get_all_admin_gender_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "gender":"Male",
            "orderby":"gender",
            "sort":"asc"
        }

        res = client.get('/user',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    # # ======================================= PUT ==================================== #

    def test_user_put_admin(self, client):
        token = create_token(True)

        data = {
                "username"		:"username07",
                "first_name"	:"leli",
                "last_name"		:"anto",
                "gender"		:"Female",
                "date_of_birth"	:"15 Oktober 1500",
                "address"		:"jl.Simpang taman Agung nomor 107",
                "city"			:"Malang",
                "zip_code"		:"65146",
                "phone_number"	:"081275988888",
                "password"		:"username3",
                "email"			:"lelianto@alterra.id"
            }

        res = client.put('/user/1', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
        self.idPerson = res_json['id']

    def test_user_put_admin_id_notfound(self, client):
        token = create_token(True)

        data = {
            "username"		:"username07",
            "first_name"	:"leli",
            "last_name"		:"anto",
            "gender"		:"Female",
            "date_of_birth"	:"15 Oktober 1500",
            "address"		:"jl.Simpang taman Agung nomor 107",
            "city"			:"Malang",
            "zip_code"		:"65146",
            "phone_number"	:"081275988888",
            "password"		:"username3",
            "email"			:"lelianto@alterra.id"
        }

        res = client.put('/user/100', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    # ======================================= DELETE ==================================== #

    def test_user_delete_id_admin(self, client):
        token = create_token(True)
        res = client.delete('/user/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_user_delete_id_admin_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/user/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # # ======================================= PATCH ==================================== #

    def test_user_patch_admin(self, client):
        token = create_token(True)
        res = client.patch('/user',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501