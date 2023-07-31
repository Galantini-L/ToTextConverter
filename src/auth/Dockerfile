FROM python:3.10-slim-bullseye

RUN apt-get update\
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --requirement ./requirements.txt
COPY server.py .

EXPOSE 5000

CMD ["python3","server.py"]