# syntax=docker/dockerfile:1
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

## Install needed packages...
RUN pip install wheel
COPY requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN pip install -r requirements.txt

COPY . /backend/

WORKDIR /backend


## See if there are any migrations, and perform them...
#RUN python manage.py makemigrations
#RUN python manage.py migrate

#RUN python manage.py runserver 0.0.0.0:8000
