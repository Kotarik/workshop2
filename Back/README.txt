nécéssaire d'installer python3, pip3, flask, request

Appli vers back 
	POST
		/reponse_alerte/0
		/reponse_alerte/1
			"etape": "inscription"
			"erreur": "tête tournée"      ou   "erreur": "delai xxxs" "
		
	GET
		/difficulte/14
			14 étant le numéro du pila



front vers back
	POST
		/reception_etat/2
			2 état un code d'erreur ( 0 = vert, 1= orange, 2= rouge)
			"pila": 14
			"etape": "inscription"
			"erreur": "tête tournée"

		/page
			"etape": "inscription"
			"pila": "14



openCV vers back

back vers OpenCV