FROM python:3.8-slim-buster

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN python -m unittest

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]