FROM python:3-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

COPY . /app/

WORKDIR /app

RUN apk add --no-cache curl curl-dev openssl-dev build-base && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    apk del build-base

CMD [ "python3", "/app/main.py" ]
