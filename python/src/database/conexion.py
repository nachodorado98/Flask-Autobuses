import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para cconfirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para obtener las lineas recorridas
	def obtenerLineasRecorridas(self, recorrida:bool=True)->Optional[List[tuple]]:

		self.c.execute("""SELECT Id_Linea, Linea, Inicio, Fin
							FROM lineas
							WHERE Recorrida=%s
							ORDER BY Id_Linea""",
							(recorrida,))

		lineas=self.c.fetchall()

		return list(map(lambda linea: (linea["id_linea"],
										linea["linea"],
										linea["inicio"],
										linea["fin"]), lineas)) if lineas else None

	# Metodo para comprobar que existe la linea
	def existe_linea(self, id_linea:int)->bool:

		self.c.execute("""SELECT *
							FROM lineas
							WHERE Id_Linea=%s""",
							(id_linea,))

		linea=self.c.fetchone()

		return False if linea is None else True

	# Metodo para añadir una linea a recorrida
	def anadirLineaRecorrida(self, id_linea:int)->None:

		self.c.execute("""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea=%s""",
							(id_linea,))

		self.confirmar()

	# Metodo para obtener el detalle de una linea
	def obtenerDetalleLinea(self, id_linea:int)->Optional[tuple]:

		self.c.execute("""SELECT Linea, Inicio, Fin, Tipo
							FROM lineas
							WHERE Id_Linea=%s""",
							(id_linea,))

		datos=self.c.fetchone()

		return None if datos is None else (datos["linea"], datos["inicio"], datos["fin"], datos["tipo"])

	# Metodo para obtener numero de paradas de una linea
	def numero_paradas(self, id_linea:int)->int:

		self.c.execute("""SELECT COUNT(1) as Numero_paradas
							FROM paradas
							WHERE Id_Linea=%s""",
							(id_linea,))

		return self.c.fetchone()["numero_paradas"]

	# Metodo para obtener numero de paradas de una linea en un sentido especifico
	def numero_paradas_sentido(self, id_linea:int, sentido:str="IDA")->int:

		self.c.execute("""SELECT COUNT(1) as Numero_paradas
							FROM paradas
							WHERE Id_Linea=%s
							AND Sentido=%s""",
							(id_linea, sentido))

		return self.c.fetchone()["numero_paradas"]

	# Metodo para saber el nombre de a linea a partir de su id
	def nombre_linea(self, id_linea:int)->Optional[str]:

		self.c.execute("""SELECT Linea as Nombre_Linea
							FROM lineas
							WHERE Id_Linea=%s""",
							(id_linea,))

		nombre=self.c.fetchone()

		return None if nombre is None else nombre["nombre_linea"]

	# Metodo para obtener las paradas que no son favoritas de una linea
	def paradas_no_favoritas(self, id_linea:int)->Optional[List[tuple]]:

		self.c.execute("""SELECT Id_Parada, Parada, Nombre, Sentido
							FROM paradas
							WHERE Id_Linea=%s
							AND Favorita=False
							ORDER BY Sentido, Parada""",
							(id_linea,))

		paradas=self.c.fetchall()

		return list(map(lambda parada: (parada["id_parada"],
										parada["parada"],
										parada["nombre"],
										parada["sentido"]), paradas)) if paradas else None

	# Metodo para comprobar que existe la parada
	def existe_parada(self, parada:int)->bool:

		self.c.execute("""SELECT *
							FROM paradas
							WHERE Parada=%s""",
							(parada,))

		parada=self.c.fetchone()

		return False if parada is None else True

	# Metodo para añadir una parada a favorita
	def anadirParadaFavorita(self, parada:int)->None:

		self.c.execute("""UPDATE paradas
							SET Favorita=True
							WHERE Parada=%s""",
							(parada,))

		self.confirmar()

	# Metodo para obtener las paradas favoritas
	def paradas_favoritas(self)->Optional[List[tuple]]:

		self.c.execute("""SELECT p.Parada, p.Nombre, p.Comentario, STRING_AGG(l.Linea, ', ') AS Lineas
							FROM paradas p
							JOIN lineas l
							USING (id_linea)
							WHERE Favorita=True
							GROUP BY p.Parada, p.Nombre, p.Comentario
							ORDER BY p.Parada""")

		paradas=self.c.fetchall()

		return list(map(lambda parada: (parada["parada"],
										parada["nombre"],
										parada["comentario"],
										parada["lineas"]), paradas)) if paradas else None

	# Metodo para eliminar una parada a favorita
	def eliminarParadaFavorita(self, parada:int)->None:

		self.c.execute("""UPDATE paradas
							SET Favorita=False
							WHERE Parada=%s""",
							(parada,))

		self.confirmar()

	# Metodo para comprobar si la parada es favorita
	def es_favorita(self, parada:int)->bool:

		self.c.execute("""SELECT *
							FROM paradas
							WHERE Parada=%s
							AND Favorita=True""",
							(parada,))

		parada=self.c.fetchone()

		return False if parada is None else True

	# Metodo para obtener el detalle de la parada 
	def detalle_parada(self, parada:int)->Optional[tuple]:

		self.c.execute("""SELECT p.Parada, p.Nombre, p.Comentario, p.Zona, p.Latitud, p.Longitud,
							p.Municipio, b.Barrio, b.Distrito, STRING_AGG(l.Linea, ', ') AS Lineas
							FROM paradas p
							JOIN lineas l
							USING (id_linea)
							JOIN barrios b
							USING (id_barrio)
							WHERE Parada=%s
							GROUP BY p.Parada, p.Nombre, p.Comentario, p.Zona, p.Latitud,
							p.Longitud, p.Municipio, b.Barrio, b.Distrito""",
							(parada,))

		parada=self.c.fetchone()

		return None if parada is None else (parada["parada"],
											parada["nombre"],
											parada["comentario"],
											parada["zona"],
											parada["latitud"],
											parada["longitud"],
											parada["municipio"],
											parada["barrio"],
											parada["distrito"],
											parada["lineas"])