FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/
COPY ./pyinv/pyinv/configuration.docker.py /app/pyinv/pyinv/configuration.py

EXPOSE 8000
RUN python3 manage.py runserver 0.0.0.0:8000
