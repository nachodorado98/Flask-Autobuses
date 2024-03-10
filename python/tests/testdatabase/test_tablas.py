import pytest

def test_obtener_lineas_recorridas_no_existentes(conexion):

	assert conexion.obtenerLineasRecorridas() is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_lineas_recorridas_existente(conexion, id_linea):

	conexion.c.execute(f"""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea={id_linea}""")

	conexion.confirmar()

	lineas=conexion.obtenerLineasRecorridas()

	assert len(lineas)==1
	assert lineas[0][0]==id_linea

def test_obtener_lineas_recorridas(conexion):

	for numero in range(1,6):

		conexion.c.execute(f"""UPDATE lineas
								SET Recorrida=True
								WHERE Id_Linea={numero}""")

	conexion.confirmar()

	lineas=conexion.obtenerLineasRecorridas()

	assert len(lineas)==5

	for numero, linea in enumerate(lineas):

		assert linea[0]==numero+1