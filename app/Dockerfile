FROM python:3.8.3-alpine
WORKDIR /app

RUN apk --no-cache add libpq gcc musl-dev

RUN set -e; \
    apk add --no-cache --virtual .compile-deps python3-dev libc-dev linux-headers; \
    pip3 install uwsgi==2.0.19.1 --no-cache-dir; \
    apk del --no-cache .compile-deps;

RUN pip3 install pipenv==2020.11.15 --no-cache-dir

COPY Pipfile* /app

RUN pipenv install --system --deploy

COPY . /app

