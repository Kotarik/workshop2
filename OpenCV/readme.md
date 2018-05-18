Détection de de visage et d'émotion via OpenCV.

## Dépendances

- OpenCV
- Python3-imutils
- Python3-dlib
- Python3-numpy
- Python3-scipy
- Python3-requests

## Utilisation

~~~Bash
facial_detectv2.py [-h] -p SHAPE_PREDICTOR [-n] [-f]
~~~

#### Aide

Afficher l'aide.

~~~Bash
-h, --help
~~~

### Prédicteur

Ficher de prédiction pour détecter les visages.

~~~Bash
-p SHAPE_PREDICTOR, --shape-predictor SHAPE_PREDICTOR
~~~

### Requête

Permet de déactiver l'envoie de requête pour la déctection d'une émotion.

~~~Bash
-n, --no-request
~~~

### Visage

Permet d'afficher les différentes partie d'un visage.

~~~Bash
-f, --face
~~~


## Référence

[PyImageSearch](https://www.pyimagesearch.com/2018/04/03/facial-landmarks-dlib-opencv-python/)
