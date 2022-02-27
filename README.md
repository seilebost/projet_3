## projet_3
PROJET N°3 / AMAZON + ELASTICSEARCH + DOCKER + API


# Comment faire 
lancer la commande `go.sh` qui effectue les actions suivantes :
* suppression de fichiers temporaires
* génération de l'image docker de l'API
* génération de l'image docker pour charger les données dans ELASTICSEARCH
* Lancement de la commande docker-compose up 
 
# Description

* Le répertoire DATA contient les fichiers nécessaires afin de créer une image DOCKER pour charger les données dans une base ELASTICSEARCH
* Le répertoire API contient les fichiers nécessaires afin de créer une image DOCKER pour créer une API d'interrogation de la base ELASTICSEARCH

# Information

* queries.sh : script unix de test unitaire pour ELASTICSEARCH
* tests/ : répertoire contenant un script python de test unitaire de l'API

## API avec FastAPI

L'API est dévelopée avec le framework [FastAPI](https://fastapi.tiangolo.com/)

