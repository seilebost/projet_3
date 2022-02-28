#!/bin/bash

echo "====> DEBUT $0"

# Suppression des fichiers temporaires 
echo ""
echo " === Nettoyage des fichiers temporaires"
rm -f amazon.json amazon_co-ecommerce_sample.csv output.html 

echo " === Construction de l'image docker pour l'API"
cd API
docker image build . -t datascientest/projet3:1.0.0

echo " === Construction de l'image docker pour la partie chargement des données"
cd ../DATA
docker image build . -t datascientest/projet3_data:1.0.0

cd ..
echo " === Arret de docker-compose"
docker-compose down

echo " === Relance de docker-compose"
docker-compose up

echo ""
echo "====> FIN $0"
