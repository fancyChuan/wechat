FROM docker.io/python:3.6
MAINTAINER fancychuan

COPY requirements.txt /
WORKDIR /

RUN pip install -r requirements.txt

ENV LANG C.UTF-8
