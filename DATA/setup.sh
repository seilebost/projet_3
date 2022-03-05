#!/bin/bash

echo "====> DEBUT $0"

# Définition de l'url (adresse+port) d'ELS
url="my_es_from_compose:9200"

# Téléchargement du fichier si absente
echo ""
echo " === Téléchargement du fichier de données si nécessaire"
cd /my_log/
if [ ! -f "./amazon_co-ecommerce_sample.csv" ]; then
	wget https://raw.githubusercontent.com/Arham-Aalam/ML-progress/master/amazon_co-ecommerce_sample.csv
fi

cd -

# Nettoyage du fichier et sa génération au format json
echo ""
echo " === Nettoyage du fichier de données dans ELS"
python3 csv2json.py

# Boucle d'attente afin de vérifier que le container ELS soit actif
while [ `curl -X GET 'my_es_from_compose:9200' | grep "You Know, for Search" | wc -l` -ne 1 ]
do
    echo "j'attends l'initialisation de l'ELS ..."
    sleep 3
done

# Suppression de l'index 
echo ""
echo " === Suppression de l'index amazon si nécessaire"
curl  -X DELETE "my_es_from_compose:9200/amazon"

# Création de l'index avec le mapping
echo ""
echo " === Création de l'index amazon dans ELS"
curl  -X PUT "my_es_from_compose:9200/amazon" -H "Content-Type: application/json" -d @mapping.json

# Insertion des données
echo ""
echo " === Insertion des données dans l'index amazon"
curl   -X PUT "my_es_from_compose:9200/amazon/_bulk" -H "Content-Type: application/json" --data-binary @/my_log/amazon.json > /my_log/output.html
printf "\n     ========= chargement des données dans ELS terminé ====================\n"

echo ""
echo "====> FIN $0"
