Appli vers back 
	POST
		/reponse_alerte/0
		/reponse_alerte/1
			"etape": "inscription"
			"erreur": "tête tournée"      ou   "erreur": "delai xxxs"  

back vers appli

front vers back
	POST
		/reception_etat/2
			"pila": 14
			"etape": "inscription"
			"erreur": "tête tournée"

back vers front

openCV vers back

back vers OpenCV