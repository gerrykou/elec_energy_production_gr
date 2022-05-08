FROM python:3.9-slim-bullseye

RUN apt-get update -y && apt-get upgrade -y

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY src src
COPY test test

CMD ["python3","-m","pytest", "-vrP"]