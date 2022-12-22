FROM python:3-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    FLASK_APP=/api.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8080 \
    MANIFEST_FILE_PATH=/app/manifest.json \
    UPRODIT_API_URL=https://api.uprodit.com

COPY . /app/

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

CMD ["python3", "-m", "flask", "run"]
