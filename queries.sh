search() { 
	curl -s -X GET 'localhost:9200/amazon/_search' -H 'Content-Type: application/json' -d "$1" | jq
}

count() {
	curl -s -X GET 'localhost:9200/amazon/_count' -H 'Content-Type: application/json' -d "$1" | jq
}

simple_search() {
	search "$1" | jq '.hits.hits[]._source | {description,number_of_reviews,product_name,product_information,manufacturer,average_review_rating,amazon_category_and_sub_category,price}'
}

simple_review_search() {
        search "$1" | jq '.hits.hits[]._source | {product_name,manufacturer,average_review_rating,amazon_category_and_sub_category,price,customer_reviews}'
}

echo -e "\ncombien d'article dans l'index ?"
count '{"query":{"match_all":{}}}' | jq '.count'

echo -e "\narticle le moins cher ?"
simple_search '{"sort":[{"price":"asc"}],"size":1,"query":{"match_all":{}}}' 

echo -e "\narticle le plus cher ?"
simple_search '{"sort":[{"price":"desc"}],"size":1,"query":{"match_all":{}}}'

echo -e "\ncombien d'article de moins de £10 ?"
count '{"query":{"range":{"price":{"lt":10}}}}' | jq '.count'

echo -e "\narticle le moins cher avec note supérieure à 4 & plus de 100 reviews ?"
simple_search '{"sort":[{"price":"asc"}],"size":1,"query":{"bool":{"must":[{"range":{"average_review_rating":{"gt":4}}},{"range":{"number_of_reviews":{"gt":100}}}]}}}'

echo -e "\narticle le plus cher de la catégorie 'Games > Card Games' avec note supérieure à 4 & plus de 100 reviews ?"
simple_search '{"sort":[{"price":"desc"}],"size":1,"query":{"bool":{"must":[{"match":{"amazon_category_and_sub_category":"Games > Card Games"}},{"range":{"average_review_rating":{"gt":4}}},{"range":{"number_of_reviews":{"gt":100}}}]}}}'

echo -e "\narticles contrefaits et de mauvaise qualité selon les reviews" 
simple_review_search '{"query":{"query_string":{"query":"counterfeit AND (bad OR poor)","fields":["customer_reviews"]}}}'
