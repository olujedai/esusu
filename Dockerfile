FROM python:3.7-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user/

COPY requirements.txt requirements.txt
RUN apk add postgresql-libs
RUN apk update && apk add --virtual .build-deps \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev && \
    pip install -r requirements.txt --no-cache-dir --timeout 60 && \
    apk --purge del .build-deps
COPY esusu esusu

EXPOSE 8000
