import unittest
from app import app, db, Colis

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_recevoir_colis(self):
        data = {'colis': [{'IDcolis': '123', 'Xadresse': 1.0, 'Yadresse': 2.0}]}
        response = self.app.post('/colis', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Colis reçus avec succès'})

        # Vérifier que le colis a été ajouté à la base de données
        colis = Colis.query.filter_by(IDcolis='123').first()
        self.assertIsNotNone(colis)
        self.assertEqual(colis.Xadresse, 1.0)
        self.assertEqual(colis.Yadresse, 2.0)

    # Ajoutez d'autres tests selon vos besoins

if __name__ == '__main__':
    unittest.main()
