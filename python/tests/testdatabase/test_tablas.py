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

def test_obtener_lineas_no_recorridas_no_existentes(conexion):

	conexion.c.execute("""UPDATE lineas
							SET Recorrida=True""")

	assert conexion.obtenerLineasRecorridas(False) is None

def test_obtener_lineas_no_recorridas(conexion):

	lineas_no_recorridas=conexion.obtenerLineasRecorridas(False)

	assert len(lineas_no_recorridas)==218

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_lineas_no_recorridas_recorrida(conexion, id_linea):

	conexion.c.execute(f"""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea={id_linea}""")

	conexion.confirmar()

	lineas_recorridas=conexion.obtenerLineasRecorridas()

	lineas_no_recorridas=conexion.obtenerLineasRecorridas(False)

	assert len(lineas_recorridas)==1
	assert len(lineas_no_recorridas)==217
	assert len(lineas_recorridas)+len(lineas_no_recorridas)==218

@pytest.mark.parametrize(["numero_lineas"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_lineas_no_recorridas_recorridas(conexion, numero_lineas):

	for numero in range(1, numero_lineas+1):

		conexion.c.execute(f"""UPDATE lineas
								SET Recorrida=True
								WHERE Id_Linea={numero}""")

	conexion.confirmar()

	lineas_recorridas=conexion.obtenerLineasRecorridas()

	lineas_no_recorridas=conexion.obtenerLineasRecorridas(False)

	assert len(lineas_recorridas)+len(lineas_no_recorridas)==218

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_existe_linea_no_existe(conexion, id_linea):

	assert not conexion.existe_linea(id_linea)

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_existe_linea_existe(conexion, id_linea):

	assert conexion.existe_linea(id_linea)

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_anadir_linea_recorrida(conexion, id_linea):

	conexion.anadirLineaRecorrida(id_linea)

	lineas_recorridas=conexion.obtenerLineasRecorridas()

	assert len(lineas_recorridas)==1