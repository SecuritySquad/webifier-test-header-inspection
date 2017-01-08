FROM debian:latest

COPY . /tmp/

RUN apt-get update -y

RUN apt-get install python3 python3-pip -y

RUN pip3 install --requirement /tmp/requirements.txt

CMD python3 /tmp/src/check.py -i $ID -u $URL