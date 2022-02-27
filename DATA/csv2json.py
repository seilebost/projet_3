import pandas as pd
import json
df = pd.read_csv("/my_log/amazon_co-ecommerce_sample.csv", sep = ",")

#Définition des champs : PRICE / AVERAGE_REVIEW_RATING / NUMBER_OF_REVIEWS en numérique
#nettoyage du champ PRICE : suppressin de £ et de la forme 'xxx - yyy' pour ne garder que xxx
df['price']=df['price'].replace('[£,]','',regex=True)
df['price']=df['price'].replace(' - .+','',regex=True).astype(float)
#nettoyage du champ AVERAGE_REVIEW_RATING : suppression de ' out of 5 stars' et de la forme 'xxx - yyy' pour ne garder que xxx
df['average_review_rating']=df['average_review_rating'].replace(' out of 5 stars','',regex=True).astype(float)
#nettoyage du champ NUMBER_OF_REVIEWS : suppression de ' out of 5 stars' et de la forme 'xxx - yyy' pour ne garder que xxx
df['number_of_reviews']=df['number_of_reviews'].replace(',','',regex=True).astype(float)

#Creation du .json
df_json= json.loads(df.to_json(orient = "records"))
with open('/my_log/amazon.json', 'w', newline='') as out:
    for i,line in enumerate(df_json):
        out.write(f'{{"index":{{"_id":"{line["uniq_id"]}"}}}}\n')
        json.dump(line,out)
        out.write('\n')
