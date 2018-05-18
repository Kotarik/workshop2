## Dépendances

- python3
- python3-requests
- python3-flask
- python3-flask-cors
- python3-flask-talisman

Via apt :

- python3
- python3-setuptools
- python3-pip

Via pip3 :

- requests
- flask
- flask-cors
- flask-talisman


## API

## ```/emotion```

### POST

Permet de remonter une émotion facial de la borne PILA vers le backend.

Entrée :
~~~python
{"emotion": "surpris", "pila": 1}
~~~


## ```/reception_etat```

### POST

Permet de remonter une erreur du frontend de la borne PILA vers le backend

Entrée :
~~~python
{"erreur": "demande_aide", "pila": 1, "etat": 2}
~~~


## ```/alerte```

### GET

Permet de récupérer la liste des bornes PILA ayant une émotion et / ou une erreur de déclaré.

Sortie :
~~~python
[{'pila' : 1}, {"pila": 2}]
~~~


## ```/reponse_alerte```

### POST

Permet de signaler un faux-positif ou non pour une erreur et / ou émotion.

Entrée :
~~~python
{"reponse": 0, "pila": 1}
~~~