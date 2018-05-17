nécéssaire d'installer python3, pip, flask, requests, flask-cors, flask-talisman

Appli vers back 
	POST
		/reponse_alerte
			"reponse": 1				ou 		"reponse": 0		0= faux positif, 1 = véritable itnervention
			"etape": "inscription"
			"erreur": "tête tournée"      ou   "erreur": "delai xxxs" 
		
	GET
		/difficulte/14
			14 étant le numéro du pila
		/alerte



front vers back
	POST
		/reception_etat
			2 état un code d'erreur ( 0 = vert, 1= orange, 2= rouge)
			"pila": 14
			"etape": "inscription"
			"erreur": "tête tournée"
			"etat": 2

		/page
			"etape": "inscription"
			"pila": "14

back vers appli



openCV vers back

back vers OpenCV