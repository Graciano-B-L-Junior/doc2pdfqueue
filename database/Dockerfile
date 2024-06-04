FROM postgres:bookworm

COPY init.sql /docker-entrypoint-initdb.d/

ENV POSTGRES_PASSWORD=example