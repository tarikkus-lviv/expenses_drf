FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app