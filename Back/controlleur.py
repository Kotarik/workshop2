#! /usr/bin/python
# -*- coding:utf-8 -*-
## nécéssaire d'installer python3, pip , flask, requests, flask-cors

import cgitb; cgitb.enable()
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

array = []

variables={
'etape' : None,
'emotion' : None,
'erreur' : None,
'pila' : None
}

#Json rempli manuellement pour le moment, mais qui devrait se remplir automatiquement par la suite
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
		},
	3: {
		'etape' : "inscription",
		'emotion' : "headturn",
		'erreur' : "null",
		'nbResultatOk' : 0,
		'nbResultatNok' : 0
		}
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
		
		#Stockage en variable pour traitement ultérieur
		variables["pila"]=request.form['pila']
		variables["etape"]=request.form['etape']
		variables["erreur"]=request.form['erreur']

		#Remplissage de l'array avec les bornes pila en erreur, et l'étape de l'erreur
		array.append({'pila':variables["pila"],'etape':variables["etape"]})

		return jsonify(
			
        	retour="besoin assistance humaine, données envoyé :",
        	data = {'pila':request.form['pila'],'etape':request.form['etape'],'erreur': request.form['erreur']}
    	), 200
	else:
		#return message d'erreur bad request
		return abort(400)

@app.route('/alerte', methods=['GET'])
def alerte():
	#fonction permetant à l'application smartphone de venir chercher les bornes en erreur listé dans l'array
		return jsonify(array), 201



@app.route('/reponse_alerte', methods=['POST'])
def reponse_alerte():
	#fonction permettant de valider la bonne information de l'erreur, ou de renseigner l'erreur en tant que faux-positif à des fin d'amélioration manuelle de la détection.
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
				if (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['erreur'] == variables["erreur"]) or (retourErreur[i]['etape'] == request.form['etape'] and retourErreur[i]['emotion'] == variables["emotion"]):
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
def emotions():
	if request.form['emotion'] == "concentre":
		variables["emotion"]=request.form['emotion']
		variables["pila"]=request.form['pila']
		array.append({'pila':variables["pila"],'etape':None})
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
    elif request.form['emotion'] == "headturn":
    	variables["emotion"]=request.form['emotion']
		variables["pila"]=request.form['pila']
		print(variables["emotion"], variables["pila"])
		return jsonify(
        	retour="headturn"
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

