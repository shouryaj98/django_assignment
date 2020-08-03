FROM python:3-alpine

WORKDIR /app

RUN pip install Django==3.0.8

COPY . /app

CMD python manage.py runserver 

