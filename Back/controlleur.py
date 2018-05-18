#! /usr/bin/python3
## nécéssaire d'installer python3, pip , flask, requests, flask-cors, flask-talisman

import cgitb; cgitb.enable()
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_talisman import Talisman

app = Flask(__name__)
CORS(app)
talisman = Talisman(app)

array = []

#Json rempli manuellement pour le moment, mais qui devrait se remplir automatiquement par la suite
retourErreur = {
}

@app.route('/')
#fonction de test de vie de l'API
def index():
    return "Hello world!"

@app.route('/reception_etat', methods=['POST'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
def reception_etat():
	#fonction permetant au site pole emploi d'envoyer au backend l'état d'une borne pila.
	if request.form['etat'] == "0":
		# pas besoin d'aide
		return jsonify(
        	retour="pas besoin d'aide"
    	), 200
  
	elif request.form['etat'] == "1":
		# besoin d'une assistance non humaine
		return jsonify(
        	retour="besoin d'une assistance non humaine"
    	), 200
	elif request.form['etat'] == "2":
		pila_nb = int(request.form['pila'])

		if pila_nb in retourErreur.keys():
			if 'erreur' in retourErreur[pila_nb].keys():
				return jsonify(
		        	retour = "Déja erreur"
		    	), 200
			else:
				pass
		else:
			retourErreur[pila_nb] = {}

		retourErreur[pila_nb]['erreur'] = request.form['erreur']

		return jsonify(
	    	retour = "Erreur enregistré"
		), 200

@app.route('/alerte', methods=['GET'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
# Fonction permettant de remplir la liste des Borne pila en erreur
def alerte():
	list_pila = []

	for k in retourErreur.keys():
		if type(k) == int:
			list_pila.append({'pila': k})
		else:
			pass

	import pprint
	pprint.pprint(list_pila)

	return jsonify(list_pila), 201

@app.route('/reponse_alerte', methods=['POST'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
# Fonction permettant au conseiller de valider depuis son application smartphone la bonne information de l'erreur, ou de renseigner l'erreur en tant que faux-positif à des fin d'amélioration manuelle de la détection. 
def reponse_alerte():
	pila_nb = int(request.form['pila'])

	erreur = retourErreur[pila_nb].get('erreur', None)
	if erreur is None:
		pass
	else:
		if erreur not in retourErreur.keys():
			retourErreur[erreur] = {
				'nbResultatNok': 0,
				'nbResultatOk': 0
				}
		else:
			pass

	emotion = retourErreur[pila_nb].get('emotion', None)
	if emotion is None:
		pass
	else:
		if emotion not in retourErreur.keys():
			retourErreur[emotion] = {
				'nbResultatNok': 0,
				'nbResultatOk': 0
				}
		else:
			pass

	
	# Si reponse = 0 L'intervention du conseiller pole emploi est un faux positif
	if request.form['reponse'] == "0":
		if erreur is not None:
			retourErreur[erreur]['nbResultatNok'] += 1
		if emotion is not None:
			retourErreur[emotion]['nbResultatNok'] += 1
	# Sinon reponse = 1 L'intervention du conseiller pole emploi est une vrai erreur
	elif request.form['reponse'] == "1":
		if erreur is not None:
			retourErreur[erreur]['nbResultatOk'] += 1
		if emotion is not None:
			retourErreur[emotion]['nbResultatOk'] += 1
	else:
		return jsonify(
		retour = "erreur dans la réponse envoyé"
		), 400
	del retourErreur[int(request.form['pila'])]

	return jsonify(
		retour = "Traitement effectué !"
		), 200


@app.route('/emotion', methods=['POST'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
# Le traitement OpenCV envoi ici les émotions
def emotions():
	pila_nb = int(request.form['pila'])

	if pila_nb in retourErreur.keys():
		if 'emotion' in retourErreur[pila_nb].keys():
			return jsonify(
	        	retour = "Déja émotion"
	    	), 200
		else:
			pass
	else:
		retourErreur[pila_nb] = {}

	retourErreur[pila_nb]['emotion'] = request.form['emotion']

	return jsonify(
    	retour = "Émotion enregistré"
	), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')