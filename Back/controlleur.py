#! /usr/bin/python
# -*- coding:utf-8 -*-
## nécéssaire d'installer python3, pip , flask, requests, flask-cors

import cgitb; cgitb.enable()
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

variables={
'etape' : None,
'emotion' : None,
'erreur' : None,
'pila' : None
}



app = Flask(__name__)
CORS(app)
listeAlerte={
	0:{
		'alerte':0
	}
}

retourErreur={
	0: {
		'etape' : "inscription",
		'emotion' : "surpris",
		'erreur' : "null",
		'nbResultatOk' : 0,
		'nbResultatNok' : 0
		},
	1: {
		'etape' : "inscription",
		'emotion' : "concentré",
		'erreur' : "null",
		'nbResultatOk' : 0,
		'nbResultatNok' : 0
		},
	
	2: {
		'etape': "inscription",
		'emotion' : "null",
		'erreur' : "demande_aide",
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
def index():
    return "Hello !"



@app.route('/reception_etat', methods=['POST'])
def reception_etat():
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
		# besoin assistance humaine, envoi requete appli reac port 8081
		#je ne peux pas push chez valentine, elle doit venir chercher en variable du contenu toutes les x secondes
		
		variables["pila"]=request.form['pila']
		variables["etape"]=request.form['etape']
		variables["erreur"]=request.form['erreur']

		return jsonify(
			
        	retour="besoin assistance humaine, données envoyé :",
        	data = {'pila':request.form['pila'],'etape':request.form['etape'],'erreur': request.form['erreur']}
    	), 200
	else:
		#return message d'erreur bad request
		return abort(400)

@app.route('/alerte', methods=['GET'])
def alerte():
		return jsonify({'pila': variables["pila"], 'etape': variables["etape"]}), 201



@app.route('/reponse_alerte', methods=['POST'])
def reponse_alerte():
	if request.form['reponse'] == "0":
		#faux positif
		#increment de l'objet json sur la variable NbRésultatNok correspondant
		#pour tout les pila dans le json retourErreur
		for i in range(len(retourErreur)):
			#si l'étape et l'erreur correspondent
			print(request.form)
			if not 'etape' in request.form:
				request.form['etape'] = "unknown"
			else:
				if (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == variables["erreur"]) or (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['emotion'] == variables["emotion"]):
					retourErreur[i]['nbResultatNok'] +=1
					variables["emotion"]=None
					variables["erreur"]=None
		return jsonify(retourErreur), 200
			
	elif request.form['reponse'] == "1":
		# véritable problème
		#increment de l'objet json sur la variable NbRésultatok correspondant
		for i in range(len(retourErreur)):
			if (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == variables["erreur"]) or (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['emotion'] == variables["emotion"]):
				retourErreur[i]['nbResultatOk'] +=1
				variables["emotion"]=None
				variables["erreur"]=None	
		return jsonify(retourErreur), 200

	else:
		#return message d'erreur bad request
		return jsonify(retour="reponse mal définit dans le post"), 400



@app.route('/emotion', methods=['POST'])
def emotions():
	if request.form['emotion'] == "concentre":
		variables["emotion"]=request.form['emotion']
		variables["pila"]=request.form['pila']
		print(variables["emotion"], variables["pila"])
		return jsonify(
        	retour="concentre"
    	), 200
	elif request.form['emotion'] == "surpris":
		variables["emotion"]=request.form['emotion']
		variables["pila"]=request.form['pila']
		print(variables["emotion"], variables["pila"])
		return jsonify(
        	retour="surpris"
    	), 200
	else : 
		return jsonify(
        	retour="mauvaise emotion"
    	), 400

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

if __name__ == '__main__':
    app.run(debug=True)

