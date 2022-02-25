#!/bin/bash


#Telechargement du fichier si absent
if [ ! -f "./amazon_co-ecommerce_sample.csv" ]; then
	wget https://raw.githubusercontent.com/Arham-Aalam/ML-progress/master/amazon_co-ecommerce_sample.csv
fi

curl -s -X DELETE "localhost:9200/amazon"

#Nettoyage du fichier et sa generation en format json
python3 csv2json.py

#Création de l'index avec le mapping
curl -s -X PUT "localhost:9200/amazon" -H "Content-Type: application/json" -d @mapping.json

#Insertion des données
curl  -s -X PUT "localhost:9200/amazon/_bulk" -H "Content-Type: application/json" --data-binary @amazon.json > output.html
printf "\n============== chargement terminé ====================\n\n"

#suppression du fichier JSON
rm amazon.json
