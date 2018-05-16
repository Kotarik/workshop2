#! /usr/bin/python
# -*- coding:utf-8 -*-
## nécéssaire d'installer python3, pip , flask, requests, flask-cors

import cgitb; cgitb.enable()
import requests
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
retourErreur={
	0: {
		'etape' : "inscription",
		'erreur' : "tête tournée",
		'nbResultatOk' : 0,
		'nbResultatNok' : 0,
		},
	
	1: {
		'etape': "inscription",
		'erreur' : "delai xxxs",
		'nbResultatOk' : 0,
		'nbResultatNok' : 0
		}
	}

statusPila={
	0: {
		'pila': "1",
		'etape' : "inscription"
	   },
	
	1: {
		'pila': "2",
		'etape' : "actualisation"
	   }
}




@app.route('/')
@crossdomain(origin='*')
def index():
    return "Hello !"

"""@app.route('/difficulte/<int:pila>' methods=['GET'])
def difficulte():
	for i in range(len(statusPila)):
		if statusPila[i]['pila'] == request.args['pila']:
			etapePila=statusPila[i]['etape']
			#comparaison avec openCV du status de l'utilisateur
			#attente réponse
				#si pas de pb, on vire les données stocké temporairment
				#si problèmene, on enregistre les données OpenCV en base (json retourErreur )
		else:
			return jsonify(
        		retour="Numero pila non trouvé en base"
    			), 400





			#code en attente
	if reponse == 0:
		#faux positif
		#increment de l'objet json sur la variable NbRésultatNok correspondant
		for i in range(len(retourErreur)):
			if retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == request.form['erreur']:
				retourErreur[i]['nbResultatNok'] +=1 
		return jsonify(retourErreur), 200
			
	elif reponse == 1:
		# véritable problème
		#increment de l'objet json sur la variable NbRésultatok correspondant
		for i in range(len(retourErreur)):
			if retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == request.form['erreur']:
				retourErreur[i]['nbResultatOk'] +=1 	
		return jsonify(retourErreur), 200

	else:
		#return message d'erreur bad request
		return abort(400)"""

@app.route('/reception_etat', methods=['GET', 'POST'])
@crossdomain(origin='*')
def reception_etat():
	session = requests.session()
	if request.form['etat'] == 0:
		# pas besoin d'aide
		return jsonify(
        	retour="pas besoin d'aide"
    	), 200
  
	elif request.form['etat'] == 1:
		# besoin d'une assistance non humaine
		return jsonify(
        	retour="besoin d'une assistance non humaine"
    	), 200
	elif request.form['etat'] == 2:
		# besoin assistance humaine, envoi requete appli reac port 8081
		#je ne peux pas push chez valentine, elle doit venir chercher en variable du contenu toutes les x secondes
		
		pila=request.form['pila']
		etape=request.form['etape']
		erreur=request.form['erreur']

		return jsonify(
			
        	retour="besoin assistance humaine, données envoyé :",
        	data = {'pila':request.form['pila'],'etape':request.form['etape'],'erreur': request.form['erreur']}
    	), 200
	else:
		#return message d'erreur bad request
		return abort(400)




@app.route('/reponse_alerte', methods=['POST'])
@crossdomain(origin='*')
def reponse_alerte():
	if request.form['reponse'] == "0":
		#faux positif
		#increment de l'objet json sur la variable NbRésultatNok correspondant
		for i in range(len(retourErreur)):
			if retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == request.form['erreur']:
				retourErreur[i]['nbResultatNok'] +=1 
		return jsonify(retourErreur), 200
			
	elif request.form['reponse'] == "1":
		# véritable problème
		#increment de l'objet json sur la variable NbRésultatok correspondant
		for i in range(len(retourErreur)):
			if retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == request.form['erreur']:
				retourErreur[i]['nbResultatOk'] +=1 	
		return jsonify(retourErreur), 200

	else:
		#return message d'erreur bad request
		return jsonify(
			
        	retour="reponse mal définit dans le post"
    	), 400

@app.route('/pick', methods=['GET'])
@crossdomain(origin='*')
def pick():
		return jsonify({'pila': pila, 'etape': etape, 'erreur': erreur}), 201

if __name__ == '__main__':
    app.run(debug=True)

