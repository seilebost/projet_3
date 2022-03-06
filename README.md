# projet_3
PROJET N°3 / AMAZON + ELASTICSEARCH + DOCKER + API


## Comment faire 
lancer la commande `go.sh` qui effectue les actions suivantes :
* suppression de fichiers temporaires
* génération de l'image docker de l'API
* génération de l'image docker pour charger les données dans ELASTICSEARCH
* Lancement de la commande docker-compose up 
 
## Description

* Le répertoire DATA contient les fichiers nécessaires afin de créer une image DOCKER pour charger les données dans une base ELASTICSEARCH
* Le répertoire API contient les fichiers nécessaires afin de créer une image DOCKER pour créer une API d'interrogation de la base ELASTICSEARCH

## Données
* Les données proviennent du site https://raw.githubusercontent.com/Arham-Aalam/ML-progress/master/amazon_co-ecommerce_sample.csv

## Information

* queries.sh : script unix de test unitaire pour ELASTICSEARCH
* tests/ : répertoire contenant un script python de test unitaire de l'API
* docker-compose.yml : fichier de paramétrage pour DOCKER permettant de lancer une base ELASTICSEARCH, un chargement de données dans celle-ci et une API sous FASTAPI pour l'interrogation de la base ELASTICSEARCH
* go.sh : script unix pour créer les images DOCKER et lancer la mise à disposition de la base de données, le chargement de données et une API d'interrogation


## API avec FastAPI

L'API est dévelopée avec le framework [FastAPI](https://fastapi.tiangolo.com/)

### Enpoints

#### /
Cet endpoint permet de contrôler si l'API est en fonctionnement
#### /docs
Fastapi fournit cet endpoint qui permet d'accèder à une documentation de l'API et de tester les différents endpoints
#### /info
Renvoie les informations des indexes présents dans la base
#### /search
Permet de requêter la base en donnant le terme de recherche et le champ dans lequelle cette recherche s'effectue. Il est possible de filtrer les champs retournés avec l'attribut **outputs**
#### /count
Renvoie le nombre de document présent dans la base. Les paramètre **index** et **q** donnent la possibilité de sélectionner l'index et d'affiner le résultat
#### /create_document/{index}
Cet endpoint permet d'ajouter un nouveau document à l'index spécifié. Les données du document sont transmises dans le corps de la requête
