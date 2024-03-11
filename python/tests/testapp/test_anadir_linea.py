import pytest

def test_pagina_anadir_lineas_recorridas(cliente, conexion):

	respuesta=cliente.get("/anadir_linea")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Añadir Nueva Linea Recorrida</h1>" in contenido
	assert "Selecciona una de las lineas" in contenido

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_anadir_lineas_recorridas_linea_recorrida(cliente, conexion, id_linea):

	conexion.c.execute(f"""UPDATE lineas
						SET Recorrida=True
						WHERE Id_Linea={id_linea}""")

	conexion.confirmar()

	respuesta=cliente.get("/anadir_linea")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Añadir Nueva Linea Recorrida</h1>" in contenido
	assert "Selecciona una de las lineas" in contenido
	assert f"<option value='{id_linea}'>Linea {id_linea}" not in contenido

def test_pagina_anadir_lineas_recorridas_todas_recorridas(cliente, conexion):

	conexion.c.execute("""UPDATE lineas
						SET Recorrida=True""")

	conexion.confirmar()

	respuesta=cliente.get("/anadir_linea")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Añadir Nueva Linea Recorrida</h1>" in contenido
	assert "Selecciona una linea" not in contenido
	assert "¡ENHORABUENA!" in contenido
	assert "Ya no hay ninguna linea por recorrer." in contenido
	assert "Has recorrido todas las lineas existentes." in contenido
	assert "Volver a Inicio" in contenido

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_pagina_insertar_linea_no_existe(cliente, conexion, id_linea):

	respuesta=cliente.post("/insertar_linea", data={"linea":id_linea})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido
	assert conexion.obtenerLineasRecorridas() is None

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_insertar_linea_existe(cliente, conexion, id_linea):

	respuesta=cliente.post("/insertar_linea", data={"linea":id_linea})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido
	assert len(conexion.obtenerLineasRecorridas())==1