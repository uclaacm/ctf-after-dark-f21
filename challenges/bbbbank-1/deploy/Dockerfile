FROM ubuntu:18.04
FROM python:3


WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app

VOLUME [ "/app" ]

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]