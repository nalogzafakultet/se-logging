from python:3.7.3

RUN apt-get update -yqq && apt-get install -yqq --no-install-recommends netcat && apt-get -q clean

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

CMD ["./entrypoint.sh"]
