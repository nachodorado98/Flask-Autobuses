CREATE DATABASE bbdd_buses;

\c bbdd_buses;

CREATE TABLE lineas (Id_Linea INT PRIMARY KEY,
					Linea VARCHAR(20),
					Inicio VARCHAR(60),
					Fin VARCHAR(60),
					Tipo VARCHAR(15),
					Recorrida BOOL);

ALTER TABLE lineas ALTER COLUMN Recorrida SET DEFAULT FALSE;

\copy lineas (Id_Linea, Linea, Inicio, Fin, Tipo) FROM '/docker-entrypoint-initdb.d/lineas.csv' WITH CSV HEADER;

CREATE TABLE barrios (Id_Barrio INT PRIMARY KEY,
					Barrio VARCHAR(50),
					Distrito VARCHAR(50));

\copy barrios (Id_Barrio, Barrio, Distrito) FROM '/docker-entrypoint-initdb.d/barrios.csv' WITH CSV HEADER;

INSERT INTO barrios (Id_Barrio, Barrio, Distrito) VALUES (0, '-', '-');

CREATE TABLE paradas(Id_Parada SERIAL PRIMARY KEY,
					Parada INT,
					Nombre VARCHAR(100),
					Comentario VARCHAR(100),
					Tipo VARCHAR(20),
					Zona VARCHAR(3),
					Latitud FLOAT,
					Longitud FLOAT,
					Municipio VARCHAR(30),
					Id_Barrio INT,
					Id_Linea INT,
					Sentido VARCHAR(10),
					Fecha DATE,
					Favorita BOOL,
					FOREIGN KEY (Id_Barrio) REFERENCES barrios (Id_Barrio) ON DELETE CASCADE,
					FOREIGN KEY (Id_Linea) REFERENCES lineas (Id_Linea) ON DELETE CASCADE);

ALTER TABLE paradas ALTER COLUMN Favorita SET DEFAULT FALSE;


\copy paradas (Parada, Nombre, Comentario, Tipo, Zona, Latitud, Longitud, Municipio, Id_Barrio, Id_Linea, Sentido, Fecha) FROM '/docker-entrypoint-initdb.d/paradas.csv' WITH CSV HEADER;