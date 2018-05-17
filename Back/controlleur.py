#! /usr/bin/python
# -*- coding:utf-8 -*-
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

variables={
'etape' : None,
'emotion' : None,
'erreur' : None,
'pila' : None
}

#Json rempli manuellement pour le moment, mais qui devrait se remplir automatiquement par la suite
retourErreur={

	}

#Json utilisé pour la route /difficulte en cours de developpement
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
		# besoin assistance humaine, stockage des données pour envoi ultérieur vers l'application smartphone
		
		variables["pila"] = int(request.form['pila'])
		pila_nb = int(request.form['pila'])
		# Si la clé pila existe dans le dictionnaire json retourErreur
		if pila_nb in retourErreur.keys():
			# On créer une sous clé erreur vide
			retourErreur[pila_nb]['erreur'] = None
			retourErreur[pila_nb]['etape'] = None
		else:
			# Sinon on créer la clé pila puis sa sous valeur emotion vide
			retourErreur[pila_nb] = dict()
			retourErreur[pila_nb]['erreur'] = None
			retourErreur[pila_nb]['etape'] = None

		if request.form['erreur'] in ["demande_aide", "delai_30s", "delai_60s"]:
			# On le récupère dans le body de la requete post
			variables["erreur"] = request.form['erreur']

		if request.form['etape'] in ["inscription", "actualisation"]:
			variables["etape"] = request.form['etape']

			# On rempli le tableau qui sera transmi à l'application smartphone
			retourErreur[pila_nb]['erreur'] = variables["erreur"]
			retourErreur[pila_nb]['etape'] = variables["etape"]
			return jsonify(
	        	retourErreur
	    	), 200
		else: 
			return jsonify(
	        	retour = "mauvaise emotion"
	    	), 400

@app.route('/alerte', methods=['GET'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
def alerte():
	#fonction permetant à l'application smartphone de venir chercher les bornes en erreur listé dans l'array
		return jsonify(array), 201



@app.route('/reponse_alerte', methods=['POST'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
def reponse_alerte():
	#fonction permettant au conseiller de valider depuis son application smartphone la bonne information de l'erreur, ou de renseigner l'erreur en tant que faux-positif à des fin d'amélioration manuelle de la détection.
	if request.form['reponse'] == "0":
		#L'intervention du conseiller pole emploi est un faux positif
		#increment de l'objet json sur la variable NbRésultatNok correspondant
		#pour tout les pila dans le json retourErreur
		for i in range(len(retourErreur)):
			#Si l'étape est vide (la détection de l'émotion ne permet pas de trouver l'étape pour le moment)
			if not 'etape' in request.form:
				#alors on place l'étape à None
				request.form['etape'] = None
			else:
				#Sinon si l'étape et l'erreur du body ou si l'étape et l'émotion du body de la requete correspondent à une ligne du json déjà créé
				if retourErreur[i]['etape'] == request.form['etape']:

					#alors on incrémente la variable indiquant que c'est un faux positif
					retourErreur[i]['nbResultatNok'] +=1
					#On vide la ligne d'erreur correspondante dans l'array qui est envoyé à l'application smartphone
					array.remove({'pila':variables["pila"],'etape':variables["etape"]})
					#On vide les variables
					variables["emotion"]=None
					variables["erreur"]=None
					variables["pila"]=None
					variables["etape"]=None
		return jsonify(retourErreur), 200
	#Si ce n'est pas un faux positif, mais un véritable problème sur une borne, On effectue le même travail que précédement, en déhors du fait que l'on incrémente la variable pour indiquer que c'est un vrai problème.
	elif request.form['reponse'] == "1":
		#véritable problème
		#increment de l'objet json sur la variable NbRésultatok correspondant
		for i in range(len(retourErreur)):
			#Si l'étape est vide (la détection de l'émotion ne permet pas de trouver l'étape pour le moment)
			if not 'etape' in request.form:
				#alors on place l'étape à None
				request.form['etape'] = None
			else:
				#Sinon si l'étape et l'erreur du body ou si l'étape et l'émotion du body de la requete correspondent à une ligne du json déjà créé
				if (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == variables["erreur"]) or (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['emotion'] == variables["emotion"]):
					#alors on incrémente la variable indiquant que c'est un faux positif
					retourErreur[i]['nbResultatOk'] +=1
					#On vide la ligne d'erreur correspondante dans l'array qui est envoyé à l'application smartphone
					array.remove({'pila':variables["pila"],'etape':variables["etape"]})
					#On vide les variables
					variables["emotion"]=None

					variables["erreur"]=None
					variables["pila"]=None
					variables["etape"]=None	
		return jsonify(retourErreur), 200

	else:
		#return message d'erreur bad request
		return jsonify(retour="reponse mal définit dans le post"), 400



@app.route('/emotion', methods=['POST'])
#sécurisation du code en https avec flask-talisman
@talisman(force_https=True)
# Le traitement OpenCV envoi ici les émotions
def emotions():
	variables["pila"] = int(request.form['pila'])
	pila_nb = int(request.form['pila'])
	# Si la clé pila existe dans le dictionnaire json retourErreur
	if pila_nb in retourErreur.keys():
		# On créer une sous clé emotion vide
		retourErreur[pila_nb]['emotion'] = None
	else:
		# Sinon on créer la clé pila puis sa sous valeur emotion vide
		retourErreur[pila_nb] = dict()
		retourErreur[pila_nb]['emotion'] = None

	if request.form['emotion'] in ["concentre", "surpris", "headturn"]:
		# On le récupère dans le body de la requete post
		variables["emotion"] = request.form['emotion']
		# On rempli le tableau qui sera transmi à l'application smartphone
		retourErreur[pila_nb]['emotion'] = variables["emotion"]

		return jsonify(retourErreur), 200
	else: 
		return jsonify(
        	retour = "mauvaise emotion"
    	), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

