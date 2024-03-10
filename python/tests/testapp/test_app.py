def test_pagina_inicial_sin_lineas_recorridas(cliente, conexion):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Lineas de Autobus Recorridas</h1>" in contenido
	assert "No hay lineas recorridas aún..." in contenido
	assert "Añadir Nueva Linea Recorrida" in contenido

def test_pagina_inicial_con_linea_recorrida(cliente, conexion):

	conexion.c.execute("""UPDATE lineas
							SET Recorrida=True
							WHERE Id_Linea=1""")

	conexion.confirmar()

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Lineas de Autobus Recorridas</h1>" in contenido
	assert "No hay lineas recorridas aún..." not in contenido
	assert "Añadir Nueva Linea Recorrida" not in contenido
	assert "Linea 1" in contenido
	assert "PLAZA DE CRISTO REY - PROSPERIDAD" in contenido

def test_pagina_inicial_con_lineas_recorridas(cliente, conexion):

	for linea in range(1,6):

		conexion.c.execute(f"""UPDATE lineas
								SET Recorrida=True
								WHERE Id_Linea={linea}""")

	conexion.confirmar()

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Lineas de Autobus Recorridas</h1>" in contenido
	assert "No hay lineas recorridas aún..." not in contenido
	assert "Añadir Nueva Linea Recorrida" not in contenido

	for linea in range(1,6):

		assert f"Linea {linea}" in contenido