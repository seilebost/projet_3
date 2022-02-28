FROM ubuntu:20.04

ADD requirements.txt api_elasticsearch.py ./

RUN apt update && apt install python3-pip -y && pip install -r requirements.txt

EXPOSE 8000

CMD ELASTIC_URL="my_es_from_compose:9200" uvicorn api_elasticsearch:api --host 0.0.0.0
