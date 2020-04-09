FROM python:3.8-slim

RUN pip install kafka-python

WORKDIR /workdir
