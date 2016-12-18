FROM debian:latest

COPY . /tmp/

RUN apt-get update -y

RUN apt-get install python python-pip -y

RUN pip install --requirement /tmp/requirements.txt

CMD python /tmp/check.py $ID $URL