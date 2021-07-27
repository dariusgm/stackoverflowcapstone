FROM python:3.9.2
MAINTAINER dariusgm
RUN apt-get update && apt-get install -y
RUN python3 -m pip install --upgrade pip
RUN pip install pipenv
WORKDIR /app
COPY Pipfile /app
RUN pipenv install --dev --python 3.9.2 --skip-lock 

