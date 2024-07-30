FROM node:18.18.2-bullseye-slim as dev

ARG UID=1000
RUN userdel node && useradd mezza --uid ${UID} -l --create-home && mkdir /client && chown mezza /client

WORKDIR /client
USER mezza
