from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['ECAMamazon']
colis_collection = db['colis']
livreurs_collection = db['livreurs']

@app.route('/colis', methods=['POST'])
def recevoir_colis():
    data = request.json
    colis_collection.insert_many(data['colis'])
    return jsonify({'message': 'Colis reçus avec succès'})

@app.route('/livreurs/<int:id_livreur>/colis', methods=['GET'])
def get_liste_colis(id_livreur):
    liste_colis_livreur = colis_collection.find({'livreur_id': id_livreur, 'etat': 0})
    return jsonify({'colis': [colis for colis in liste_colis_livreur]})

@app.route('/livreurs/<int:id_livreur>/geolocalisation', methods=['POST'])
def update_geolocalisation(id_livreur):
    data = request.json
    livreurs_collection.update_one({'_id': id_livreur}, {'$set': {'x': data['x'], 'y': data['y']}})
    return jsonify({'message': 'Géolocalisation mise à jour avec succès'})

@app.route('/colis/<int:id_colis>/livraison', methods=['POST'])
def update_etat_livraison(id_colis):
    data = request.json
    colis_collection.update_one({'_id': id_colis}, {'$set': {'etat': data['etat']}})

    # Effectuer un POST vers une autre API
    autre_api_url = "https://url_de_l_autre_api"
    payload = {'id_colis': id_colis, 'etat': data['etat']}
    
    try:
        response = requests.post(autre_api_url, json=payload)
        response.raise_for_status()
        return jsonify({'message': 'État de livraison mis à jour avec succès et POST effectué avec succès vers l\'autre API'})
    except requests.exceptions.RequestException as e:
        return jsonify({'message': f'État de livraison mis à jour avec succès, mais erreur lors du POST vers l\'autre API: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
