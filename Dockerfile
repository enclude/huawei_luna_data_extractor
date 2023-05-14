# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
COPY run.sh run.sh
RUN pip3 install -r requirements.txt
RUN chmod a+x run.sh

COPY . .

CMD [ "./run.sh" ]
