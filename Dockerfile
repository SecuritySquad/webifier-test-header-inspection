FROM debian:latest

COPY . /tmp/

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install --requirement /tmp/requirements.txt

CMD python3 /tmp/src/check.py -i $ID -u $URL