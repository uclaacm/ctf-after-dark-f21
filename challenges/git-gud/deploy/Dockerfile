FROM python:3-slim

ADD . /ctf
WORKDIR /ctf

RUN tar -xvzf git.tar.gz
RUN rm git.tar.gz Dockerfile
RUN pip3 install -r requirements.txt

EXPOSE 3000

CMD ["gunicorn", "-c", "gunicorn.conf", "main:app"]
