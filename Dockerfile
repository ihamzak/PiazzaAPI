FROM python:3

ENV  PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /CODE
COPY . /CODE/
RUN  pip install -r requirements.txt