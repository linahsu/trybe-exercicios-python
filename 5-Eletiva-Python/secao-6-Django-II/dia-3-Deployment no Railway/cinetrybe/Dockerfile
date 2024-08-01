FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update \
    && apt install -y python3-dev netcat-openbsd default-libmysqlclient-dev build-essential pkg-config \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

# CMD [ "gunicorn", "cinetrybe.wsgi", "--bind", "0.0.0.0:8000" ]
CMD [ "sh", "entrypoint.sh" ]