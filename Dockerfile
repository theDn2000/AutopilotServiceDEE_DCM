FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt