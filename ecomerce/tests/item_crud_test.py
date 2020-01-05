import json
from . import client, create_token, reset_db

class TestItemCrud():

    idPerson = 0
    reset_db()

    # ======================================= POST ==================================== #

    def test_item_post_admin(self, client):
        token = create_token(True)

        data = {
                "item_name"		:"CARGLOSS YR HC Gothic Helm Half Face - Espresso Brown SG [L]",
                "price"			:"185000",
                "kategori"		:"OTOMOTIF",
                "deskripsi"		:"CARGLOSS YR Gothic Helm Half Face - Espresso Brown SG merupakan helm half face berbahan ABS thermoplastic yang didesain retro. Helm juga dilengkapi dengan visor yang dapat melindungi Anda dari sinar matahari. Bagian dalam helm dapat dilepas sehingga memudahkan Anda jika ingin mencucinya. Tali pengikat kuat untuk memberikan keamanan dan kenyamanan ekstra saat menggunakannya.",
                "spesifikasi_1"	:"Tipe helm Half Face",
                "spesifikasi_2"	:"berbahan ABS thermoplastic",
                "spesifikasi_3"	:"Washable",
                "gambar_1"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABFgAAABQAFhNfYgAA-gE.jpg",
                "gambar_2"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgAA9AAAABsAFJe2fQAA0-w.jpg",
                "gambar_3"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABHwAAABwAFjc1cgAAtZI.jpg",
                "gambar_4"		:"https://img14.jd.id/Indonesia/s160x160_/nHBfsgABFAAAAAwAKzU9RwAAnAE.jpg"
            }

        res = client.post('/item', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
        self.idPerson = res_json['id']

    # # ======================================= GET ==================================== #

    def test_item_get_id_admin(self, client):
        token = create_token(True)
        res = client.get('/item/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_item_get_id_admin_id_outrange(self, client):
        token = create_token(True)
        res = client.get('/item/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # ======================================= GET_All ==================================== #

    def test_item_get_all_admin_item_name_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "item_name":"CARGLOSS YR HC Gothic Helm Half Face - Espresso Brown SG [L]",
            "orderby":"item_name",
            "sort":"desc"
        }

        res = client.get('/item',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_item_get_all_admin_item_name_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "item_name":"Male",
            "orderby":"item_name",
            "sort":"asc"
        }

        res = client.get('/item',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_item_get_all_admin_price_desc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "item_name":"Male",
            "orderby":"price",
            "sort":"desc"
        }

        res = client.get('/item',query_string = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
     
        assert res.status_code == 200

    def test_item_get_all_admin_price_asc(self, client):
        token = create_token(True)

        data = {
            "p":1,
            "rp":25,
            "item_name":"Male",
            "orderby":"price",
            "sort":"asc"
        }

        res = client.get('/item',query_string= data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200


    # ======================================= PUT ==================================== #

    def test_item_put_admin(self, client):
        token = create_token(True)

        data = {
                "item_name"		:"CARGLOic Helm Half Face - Espresso Brown SG [L]",
                "price"			:"185000",
                "kategori"		:"OTOMOTIF",
                "deskripsi"		:"CARGLOSS YR Gothic Helm Half Face - Espresso Brown SG merupakan helm half face berbahan ABS thermoplastic yang didesain retro. Helm juga dilengkapi dengan visor yang dapat melindungi Anda dari sinar matahari. Bagian dalam helm dapat dilepas sehingga memudahkan Anda jika ingin mencucinya. Tali pengikat kuat untuk memberikan keamanan dan kenyamanan ekstra saat menggunakannya.",
                "spesifikasi_1"	:"Tipe helm Half Face",
                "spesifikasi_2"	:"berbahan ABS thermoplastic",
                "spesifikasi_3"	:"Washable",
                "gambar_1"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABFgAAABQAFhNfYgAA-gE.jpg",
                "gambar_2"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgAA9AAAABsAFJe2fQAA0-w.jpg",
                "gambar_3"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABHwAAABwAFjc1cgAAtZI.jpg",
                "gambar_4"		:"https://img14.jd.id/Indonesia/s160x160_/nHBfsgABFAAAAAwAKzU9RwAAnAE.jpg"
            }

        res = client.put('/item/1', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200
        assert res_json['id']>0
        
        self.idPerson = res_json['id']

    def test_item_put_admin_id_notfound(self, client):
        token = create_token(True)

        data = {
                "item_name"		:"CARGLOSS YR - Espresso Brown SG [L]",
                "price"			:"185000",
                "kategori"		:"OTOMOTIF",
                "deskripsi"		:"CARGLOSS YR Gothic Helm Half Face - Espresso Brown SG merupakan helm half face berbahan ABS thermoplastic yang didesain retro. Helm juga dilengkapi dengan visor yang dapat melindungi Anda dari sinar matahari. Bagian dalam helm dapat dilepas sehingga memudahkan Anda jika ingin mencucinya. Tali pengikat kuat untuk memberikan keamanan dan kenyamanan ekstra saat menggunakannya.",
                "spesifikasi_1"	:"Tipe helm Half Face",
                "spesifikasi_2"	:"berbahan ABS thermoplastic",
                "spesifikasi_3"	:"Washable",
                "gambar_1"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABFgAAABQAFhNfYgAA-gE.jpg",
                "gambar_2"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgAA9AAAABsAFJe2fQAA0-w.jpg",
                "gambar_3"		:"https://img20.jd.id/Indonesia/s70x70_/nHBfsgABHwAAABwAFjc1cgAAtZI.jpg",
                "gambar_4"		:"https://img14.jd.id/Indonesia/s160x160_/nHBfsgABFAAAAAwAKzU9RwAAnAE.jpg"
            }

        res = client.put('/item/100', json = data,
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 404
        
    # # ======================================= DELETE ==================================== #

    def test_item_delete_id_admin(self, client):
        token = create_token(True)
        res = client.delete('/item/1',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        
        assert res.status_code == 200

    def test_item_delete_id_admin_idnotfound(self, client):
        token = create_token(True)
        res = client.delete('/item/100',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 404

    # ======================================= PATCH ==================================== #

    def test_item_patch_admin(self, client):
        token = create_token(True)
        res = client.patch('/item',
        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
       
        assert res.status_code == 501