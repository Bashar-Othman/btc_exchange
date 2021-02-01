FROM alpine:3.7
RUN apk update && \
    apk add --no-cache bash libffi-dev postgresql-client python3 py3-psycopg2 && \
    mkdir /btc_exchange
ADD . /btc_exchange
WORKDIR /btc_exchange
RUN pip3 install -r docker.requirements.txt && chmod +x wait-for-postgres.sh manage.py
ENV APP_KEY=GF42H1N71LWVF2MS
EXPOSE 5000


