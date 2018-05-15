#! /usr/bin/python
# -*- coding:utf-8 -*-
## nécéssaire d'installer python3, pip3, flask, request

import cgitb; cgitb.enable()

from flask import Flask, request
from flask import jsonify

app = Flask(__name__)

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




@app.route('/')
def index():
    return "Hello !"

@app.route('/reception_etat/<int:etat>', methods=['GET', 'POST'])
def reception_etat(etat):
	if request.methode == 'GET' and etat == 0:
		# pas besoin d'aide
		return jsonify(
        	retour="pas besoin d'aide"
    	), 200
  
	elif etat == 1:
		# besoin d'une assistance non humaine
		return jsonify(
        	retour="besoin d'une assistance non humaine"
    	), 200
	elif etat == 2:
		# besoin assistance humaine, envoi requete appli reac port 8081

		request.post('http://localhost:8081/alerte', data = {'pila':request.form['pila'],'etape':request.form['etape'],'erreur': request.form['erreur']})
		return jsonify(
			
        	retour="besoin assistance humaine"
    	), 200
	else:
		#return message d'erreur bad request
		return abort(400)

@app.route('/reponse_alerte/<int:reponse>', methods=['POST'])
def reponse_alerte(reponse):
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
		return abort(400)

if __name__ == '__main__':
    app.run(debug=True)

