FROM apline:latest

COPY . /tmp/
RUN pip install --requirement /tmp/requirements.txt

RUN apt-get update-y


CMD python