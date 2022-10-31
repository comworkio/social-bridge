FROM python:3-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    UPRODIT_API_URL=https://api.uprodit.com

COPY . /app/

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

CMD [ "python3", "/app/main.py" ]
