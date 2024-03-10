FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/
COPY data/lineas_bus.csv /docker-entrypoint-initdb.d/lineas.csv
COPY data/barrios_madrid.csv /docker-entrypoint-initdb.d/barrios.csv
COPY data/paradas_bus.csv /docker-entrypoint-initdb.d/paradas.csv