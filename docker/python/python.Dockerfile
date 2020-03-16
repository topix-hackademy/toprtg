FROM python:3.8-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y librrd-dev libpython3-dev

COPY app/requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
