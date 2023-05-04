# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /backend/

WORKDIR /backend

## Install needed packages...
RUN pip install wheel
RUN pip install -r requirements.txt

## See if there are any migrations, and perform them...
#RUN python manage.py makemigrations
#RUN python manage.py migrate

#RUN python manage.py runserver 0.0.0.0:8000
