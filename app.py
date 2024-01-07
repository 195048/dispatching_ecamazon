from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import requests


app = Flask(__name__)
# Example database configuration in app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@db:3306/Ecamazon'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Colis(db.Model):
    __tablename__ = 'colis'
    _id = db.Column(db.Integer, primary_key=True)
    IDcolis = db.Column(db.String(50))
    Xadresse = db.Column(db.Float)
    Yadresse = db.Column(db.Float)
    etat = db.Column(db.Integer, default=0)
    livreur_id = db.Column(db.Integer)

class Livreur(db.Model):
    __tablename__ = 'livreurs'
    _id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)

# Création des tables au lancement de l'application
with app.app_context():
    db.create_all()
    initial_livreur = Livreur(x=0.0, y=0.0)
    db.session.add(initial_livreur)
    db.session.commit()


def get_all_parcels():
    try:
        # Fetch all parcels from the database using Flask-SQLAlchemy
        parcels = Colis.query.all()
        
        # Convert the SQLAlchemy objects to a list of dictionaries
        parcels_list = [
            {'_id': colis._id, 'IDcolis': colis.IDcolis, 'Xadresse': colis.Xadresse, 'Yadresse': colis.Yadresse}
            for colis in parcels
        ]

        return parcels_list
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/get_parcels', methods=['GET'])
def get_parcels():
    parcels = get_all_parcels()
    return render_template('parcels.html', parcels=parcels)
    
@app.route('/colis', methods=['POST'])
def recevoir_colis():
    data = request.json
    for colis in data['colis']:
        livreur = Livreur.query.order_by(func.random()).first()  # Example: Select a random livreur

        # Create a new parcel and associate it with the selected courier
        new_colis = Colis(IDcolis=colis['IDcolis'], Xadresse=colis['Xadresse'], Yadresse=colis['Yadresse'], livreur_id=livreur._id)
        db.session.add(new_colis)
    
    db.session.commit()
    return jsonify({'message': 'Colis reçus avec succès'})

@app.route('/livreurs/<int:id_livreur>/colis', methods=['GET'])
def get_liste_colis(id_livreur):
    liste_colis_livreur = Colis.query.filter_by(livreur_id=id_livreur, etat=0).all()
    
    colis_list = [{'_id': colis._id, 'Xadresse': colis.Xadresse, 'Yadresse': colis.Yadresse} for colis in liste_colis_livreur]
    
    return jsonify({'colis': colis_list})

@app.route('/livreurs/<int:id_livreur>/geolocalisation', methods=['POST'])
def update_geolocalisation(id_livreur):
    data = request.json
    livreur = Livreur.query.get(id_livreur)
    if livreur:
        livreur.x = data['x']
        livreur.y = data['y']
        db.session.commit()
        return jsonify({'message': 'Géolocalisation mise à jour avec succès'})
    else:
        return jsonify({'message': 'Livreur non trouvé'})

@app.route('/colis/<int:id_colis>/livraison', methods=['POST'])
def update_etat_livraison(id_colis):
    data = request.json
    colis = Colis.query.get(id_colis)
    if colis:
        colis.etat = data['etat']
        db.session.commit()

        # Effectuer un POST vers une autre API
        autre_api_url = "https://url_de_l_autre_api"
        payload = {'id_colis': id_colis, 'etat': data['etat']}
        
        try:
            response = requests.post(autre_api_url, json=payload)
            response.raise_for_status()
            return jsonify({'message': 'État de livraison mis à jour avec succès et POST effectué avec succès vers l\'autre API'})
        except requests.exceptions.RequestException as e:
            return jsonify({'message': f'État de livraison mis à jour avec succès, mais erreur lors du POST vers l\'autre API: {str(e)}'})
    else:
        return jsonify({'message': 'Colis non trouvé'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
