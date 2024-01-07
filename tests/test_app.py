import pytest
from app import app, db, Colis, Livreur
from flask import json
from unittest.mock import patch, MagicMock


@pytest.fixture
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@db:3306/Ecamazon'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()


def add_dummy_data():
    livreur = Livreur(x=0.0, y=0.0)
    colis = Colis(IDcolis='123', Xadresse=1.0, Yadresse=1.0, livreur_id=1)
    db.session.add(livreur)
    db.session.add(colis)
    db.session.commit()


def test_get_parcels(test_client):
    add_dummy_data()
    response = test_client.get('/get_parcels')
    assert response.status_code == 200



def test_recevoir_colis(test_client):
    with patch('app.Livreur.query') as mock_query:
        mock_query.order_by.return_value.first.return_value = Livreur(x=0.0, y=0.0, _id=1)
        data = {'colis': [{'IDcolis': '123', 'Xadresse': 1.0, 'Yadresse': 1.0}]}
        response = test_client.post('/colis', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'Colis reçus avec succès'


def test_get_liste_colis(test_client):
    add_dummy_data()
    response = test_client.get('/livreurs/1/colis')
    assert response.status_code == 200



def test_update_geolocalisation(test_client):
    add_dummy_data()
    data = {'x': 2.0, 'y': 2.0}
    response = test_client.post('/livreurs/1/geolocalisation', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200



def test_update_etat_livraison(test_client):
    add_dummy_data()
    data = {'etat': 1}
    with patch('requests.post') as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        response = test_client.post('/colis/1/livraison', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

