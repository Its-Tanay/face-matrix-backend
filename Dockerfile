FROM python:3.9.6

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /facial-recognition-backend

COPY ./requirements.txt /requirements.txt

RUN apt-get update \
    && pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src /facial-recognition-backend/src