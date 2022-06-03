FROM python:latest

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir apscheduler && \
    pip install --no-cache-dir requests

CMD mkdir /app
WORKDIR /app

COPY ./web/app.py /app

ENV WEB_HOST=0.0.0.0
ENV WEB_PORT=8080
ENV WEB_CHECK_TIMEOUT=60
ENV WEB_ERROR_TIMEOUT=2
ENV WEB_HOST_LIST="192.168.1.1:8080 192.168.10.10:9090 127.0.0.1:8080"

EXPOSE 8080/tcp

CMD python3 /app/app.py
