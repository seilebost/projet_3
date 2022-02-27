FROM ubuntu:20.04

WORKDIR /my_log/

WORKDIR /

ADD csv2json.py mapping.json setup.sh  ./
RUN chmod +x ./setup.sh
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN pip install --no-cache-dir pandas
RUN apt-get install curl -y
RUN apt-get install wget -y

CMD ./setup.sh 

