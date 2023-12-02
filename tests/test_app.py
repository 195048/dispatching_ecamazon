import unittest
import json
from app import app, colis_collection, livreurs_collection

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.livreur_id = 1
        self.colis_id = 1

    def test_recevoir_colis(self):
        data = {'colis': [{'_id': self.colis_id, 'Xadresse': 1, 'Yadresse': 1}]}
        response = self.app.post('/colis', json=data)
        self.assertEqual(response.status_code, 200)

        # Vérifie que le colis est bien dans la base de données
        colis = colis_collection.find_one({'_id': self.colis_id})
        self.assertIsNotNone(colis)

    def test_get_liste_colis(self):
        # Ajoute un colis pour le livreur
        colis_collection.insert_one({'_id': self.colis_id, 'Xadresse': 1, 'Yadresse': 1, 'livreur_id': self.livreur_id, 'etat': 0})

        response = self.app.get(f'/livreurs/{self.livreur_id}/colis')
        data = json.loads(response.get_data(as_text=True))

        self.assertEqual(response.status_code, 200)
        self.assertIn('colis', data)
        self.assertEqual(len(data['colis']), 1)

    def test_update_geolocalisation(self):
        data = {'x': 2, 'y': 2}
        response = self.app.post(f'/livreurs/{self.livreur_id}/geolocalisation', json=data)
        self.assertEqual(response.status_code, 200)

        # Vérifie que la géolocalisation du livreur est mise à jour dans la base de données
        livreur = livreurs_collection.find_one({'_id': self.livreur_id})
        self.assertIsNotNone(livreur)
        self.assertEqual(livreur['x'], data['x'])
        self.assertEqual(livreur['y'], data['y'])

    def test_update_etat_livraison(self):
        data = {'etat': 1}
        response = self.app.post(f'/colis/{self.colis_id}/livraison', json=data)
        self.assertEqual(response.status_code, 200)

        # Vérifie que l'état de livraison du colis est mis à jour dans la base de données
        colis = colis_collection.find_one({'_id': self.colis_id})
        self.assertIsNotNone(colis)
        self.assertEqual(colis['etat'], data['etat'])

if __name__ == '__main__':
    unittest.main()
