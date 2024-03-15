import pytest

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_pagina_anadir_parada_no_existe(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/anadir_parada/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_anadir_parada_existen(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/anadir_parada/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"<h1>Añadir Parada Favorita Linea {id_linea}</h1>" in contenido
	assert "Selecciona una de las paradas" in contenido
	assert "Añadir parada" in contenido
	assert "Cancelar" in contenido

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_anadir_parada_todas_favoritas(cliente, conexion, id_linea):

	conexion.c.execute(f"""UPDATE paradas
							SET Favorita=True
							WHERE Id_Linea={id_linea}""")

	conexion.confirmar()

	respuesta=cliente.get(f"/anadir_parada/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"<h1>Añadir Parada Favorita Linea {id_linea}</h1>" in contenido
	assert "Selecciona una de las paradas" not in contenido
	assert "Añadir parada" not in contenido
	assert "Cancelar" not in contenido
	assert "¡VAYAAA!" in contenido
	assert "Parece que ya no hay mas paradas de esta linea para escoger" in contenido

@pytest.mark.parametrize(["parada"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_pagina_insertar_parada_no_existe(cliente, conexion, parada):

	respuesta=cliente.post(f"/insertar_parada", data={"parada":parada})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada"],
	[(1,),(70,),(2011,),(356,)]
)
def test_pagina_insertar_parada_existe(cliente, conexion, parada):

	respuesta=cliente.post(f"/insertar_parada", data={"parada":parada})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

	conexion.c.execute("""SELECT Parada
							FROM paradas
							WHERE Favorita=True""")

	parada_favorita=conexion.c.fetchone()["parada"]

	assert parada==parada_favorita
