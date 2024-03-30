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

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_obtener_detalle_linea_no_existe(conexion, id_linea):

	assert conexion.obtenerDetalleLinea(id_linea) is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_detalle_linea(conexion, id_linea):

	datos=conexion.obtenerDetalleLinea(id_linea)

	assert len(datos)==4

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_numero_paradas_linea_no_tiene(conexion, id_linea):

	assert conexion.numero_paradas(id_linea)==0

@pytest.mark.parametrize(["id_linea", "paradas"],
	[
		(1, 60),
		(34, 82),
		(9, 70),
		(139, 47)
	]
)
def test_numero_paradas_linea(conexion, id_linea, paradas):

	assert conexion.numero_paradas(id_linea)==paradas

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_numero_paradas_linea_sentido_ida_no_tiene(conexion, id_linea):

	assert conexion.numero_paradas_sentido(id_linea)==0

@pytest.mark.parametrize(["id_linea", "paradas"],
	[
		(1, 30),
		(34, 41),
		(9, 34),
		(139, 23)
	]
)
def test_numero_paradas_linea_sentido_ida(conexion, id_linea, paradas):

	assert conexion.numero_paradas_sentido(id_linea)==paradas

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_numero_paradas_linea_sentido_vuelta_no_tiene(conexion, id_linea):

	assert conexion.numero_paradas_sentido(id_linea, "VUELTA")==0

@pytest.mark.parametrize(["id_linea", "paradas"],
	[
		(1, 30),
		(34, 41),
		(9, 36),
		(139, 24)
	]
)
def test_numero_paradas_linea_sentido_vuelta(conexion, id_linea, paradas):

	assert conexion.numero_paradas_sentido(id_linea, "VUELTA")==paradas

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_nombre_linea_no_existe(conexion, id_linea):

	assert conexion.nombre_linea(id_linea) is None

@pytest.mark.parametrize(["id_linea", "linea"],
	[
		(1,"1"),
		(34,"34"),
		(68,"C1"),
		(69,"C2")
	]
)
def test_nombre_linea(conexion, id_linea, linea):

	assert conexion.nombre_linea(id_linea)==linea

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_paradas_no_favoritas_no_existe(conexion, id_linea):

	assert conexion.paradas_no_favoritas(id_linea) is None

@pytest.mark.parametrize(["id_linea", "paradas"],
	[
		(1, 60),
		(34, 82),
		(9, 70),
		(139, 47)
	]
)
def test_paradas_no_favoritas_sin_favoritas(conexion, id_linea, paradas):

	paradas_no_favoritas=conexion.paradas_no_favoritas(id_linea)

	assert len(paradas_no_favoritas)==paradas

@pytest.mark.parametrize(["id_linea", "parada", "paradas"],
	[
		(1, 70, 60),
		(34, 356, 82),
		(9, 2011, 70),
		(139, 650, 47)
	]
)
def test_paradas_no_favoritas_una_favorita(conexion, id_linea, parada, paradas):

	conexion.c.execute(f"""UPDATE paradas
							SET Favorita=True
							WHERE Parada={parada}
							AND Id_Linea={id_linea}""")

	conexion.confirmar()

	paradas_no_favoritas=conexion.paradas_no_favoritas(id_linea)

	assert len(paradas_no_favoritas)==paradas-1

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_paradas_no_favoritas_todas_favoritas(conexion, id_linea):

	conexion.c.execute(f"""UPDATE paradas
							SET Favorita=True
							AND Id_Linea={id_linea}""")

	conexion.confirmar()

	assert conexion.paradas_no_favoritas(id_linea) is None


@pytest.mark.parametrize(["parada"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_existe_parada_no_existe(conexion, parada):

	assert not conexion.existe_parada(parada)

@pytest.mark.parametrize(["parada"],
	[(1,),(70,),(356,),(2011,)]
)
def test_existe_parada_existe(conexion, parada):

	assert conexion.existe_parada(parada)

@pytest.mark.parametrize(["parada", "numero_paradas"],
	[
		(1,1),
		(70,15),
		(2011,3),
		(356,2)]
)
def test_anadir_parada_favorita(conexion, parada, numero_paradas):

	conexion.anadirParadaFavorita(parada)

	conexion.c.execute("""SELECT Parada
						FROM paradas
						WHERE Favorita=True""")

	paradas_favoritas=conexion.c.fetchall()

	assert len(paradas_favoritas)==numero_paradas

	for parada_favorita in paradas_favoritas:

		assert parada_favorita["parada"]==parada

def test_paradas_favoritas_no_existen(conexion):

	assert conexion.paradas_favoritas() is None

@pytest.mark.parametrize(["parada", "numero_paradas"],
	[
		(1,1),
		(70,15),
		(2011,3),
		(356,2)]
)
def test_parada_favorita(conexion, parada, numero_paradas):

	conexion.anadirParadaFavorita(parada)

	paradas=conexion.paradas_favoritas()

	assert len(paradas)==1

	lineas=paradas[0][3].split(", ")

	assert len(lineas)==numero_paradas

@pytest.mark.parametrize(["parada"],
	[(1,),(70,),(2011,),(356,)]
)
def test_eliminar_parada_favorita(conexion, parada):

	conexion.anadirParadaFavorita(parada)

	paradas=conexion.paradas_favoritas()

	assert len(paradas)==1
	assert paradas[0][0]==parada

	conexion.eliminarParadaFavorita(parada)

	assert conexion.paradas_favoritas() is None

@pytest.mark.parametrize(["parada"],
	[(1,),(70,),(356,),(2011,)]
)
def test_no_es_favorita(conexion, parada):

	assert not conexion.es_favorita(parada)

@pytest.mark.parametrize(["parada"],
	[(1,),(70,),(356,),(2011,)]
)
def test_es_favorita(conexion, parada):

	conexion.anadirParadaFavorita(parada)

	assert conexion.es_favorita(parada)

@pytest.mark.parametrize(["parada"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_detalle_parada_no_existe(conexion, parada):

	assert conexion.detalle_parada(parada) is None

@pytest.mark.parametrize(["parada", "numero_paradas"],
	[
		(1,1),
		(70,15),
		(2011,3),
		(356,2)]
)
def test_detalle_parada_existe(conexion, parada, numero_paradas):

	parada=conexion.detalle_parada(parada)

	lineas=parada[-1].split(", ")

	assert len(lineas)==numero_paradas

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_paradas_linea_sentido_no_existe(conexion, id_linea):

	assert conexion.paradas_linea_sentido(id_linea) is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_paradas_linea_sentido_existe_ida(conexion, id_linea):

	paradas_ida=conexion.paradas_linea_sentido(id_linea)

	numero_paradas_ida=conexion.numero_paradas_sentido(id_linea)

	assert len(paradas_ida)==numero_paradas_ida

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_paradas_linea_sentido_existe_vuelta(conexion, id_linea):

	paradas_vuelta=conexion.paradas_linea_sentido(id_linea, "VUELTA")

	numero_paradas_vuelta=conexion.numero_paradas_sentido(id_linea, "VUELTA")

	assert len(paradas_vuelta)==numero_paradas_vuelta

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_obtener_recorrido_linea_no_existe(conexion, id_linea):

	assert conexion.obtenerRecorridoLinea(id_linea) is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_obtener_recorrido_linea_existe(conexion, id_linea):

	paradas_ida, paradas_vuelta=conexion.obtenerRecorridoLinea(id_linea)

	numero_paradas_ida=conexion.numero_paradas_sentido(id_linea)

	numero_paradas_vuelta=conexion.numero_paradas_sentido(id_linea, "VUELTA")

	assert len(paradas_ida)==numero_paradas_ida
	assert len(paradas_vuelta)==numero_paradas_vuelta

	numero_paradas=conexion.numero_paradas(id_linea)

	assert numero_paradas==numero_paradas_ida+numero_paradas_vuelta

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_barrios_linea_no_existe(conexion, id_linea):

	assert not conexion.barrios_linea(id_linea)

@pytest.mark.parametrize(["id_linea", "numero_barrios"],
	[
		(1, 15),
		(34, 12),
		(9, 13),
		(139, 6)
	]
)
def test_barrios_linea_existe(conexion, id_linea, numero_barrios):

	barrios=conexion.barrios_linea(id_linea)

	assert len(barrios)==numero_barrios

def test_obtener_paradas_todas_paradas(conexion):

	paradas=conexion.obtener_paradas()

	assert len(paradas)==4802

@pytest.mark.parametrize(["parada_evitar"],
	[(1,),(70,),(356,),(2011,)]
)
def test_obtener_paradas_evitando_parada(conexion, parada_evitar):

	paradas=conexion.obtener_paradas(parada_evitar)

	assert len(paradas)==4801