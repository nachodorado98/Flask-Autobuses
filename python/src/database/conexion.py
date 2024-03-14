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
							WHERE Id_Linea=%s;""",
							(id_linea,))

		return self.c.fetchone()["numero_paradas"]

		# Metodo para obtener numero de paradas de una linea en un sentido especifico
	def numero_paradas_sentido(self, id_linea:int, sentido:str="IDA")->int:

		self.c.execute("""SELECT COUNT(1) as Numero_paradas
							FROM paradas
							WHERE Id_Linea=%s
							AND Sentido=%s;""",
							(id_linea, sentido))

		return self.c.fetchone()["numero_paradas"]