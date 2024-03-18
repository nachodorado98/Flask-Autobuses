import pytest

def test_pagina_parada_favorita_sin_paradas_favoritas(cliente, conexion):

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Paradas Favoritas</h1>" in contenido
	assert "No hay paradas favoritas añadidas todavía..." in contenido
	assert "Volver" in contenido

def test_pagina_parada_favorita_con_parada_favorita(cliente, conexion):

	cliente.post(f"/insertar_parada", data={"parada":356})

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Paradas Favoritas</h1>" in contenido
	assert "No hay paradas favoritas añadidas todavía..." not in contenido
	assert "Volver" not in contenido
	assert "Nº 356" in contenido
	assert "JOAQUIN TURINA-POLVORANCA" in contenido
	assert "Joaquín Turina, 37" in contenido
	assert "Lineas: " in contenido
	assert "139" in contenido
	assert "34" in contenido

@pytest.mark.parametrize(["paradas"],
	[
		([1, 70, 2011, 356],),
		([13, 220, 2020, 330],),
		([22, 870, 2111, 321],)
	]
)
def test_pagina_parada_favorita_con_paradas_favoritas(cliente, conexion, paradas):

	for parada in paradas:

		cliente.post(f"/insertar_parada", data={"parada":parada})

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Paradas Favoritas</h1>" in contenido
	assert "No hay paradas favoritas añadidas todavía..." not in contenido
	assert "Volver" not in contenido

	for parada in paradas:

		assert f"Nº {parada}" in contenido

def test_pagina_parada_favorita_eliminar_parada_favorita(cliente, conexion):

	cliente.post(f"/insertar_parada", data={"parada":356})

	cliente.get(f"/eliminar_parada_favorita/356")

	respuesta=cliente.get("/paradas_favoritas")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Paradas Favoritas</h1>" in contenido
	assert "No hay paradas favoritas añadidas todavía..." in contenido
	assert "Volver" in contenido