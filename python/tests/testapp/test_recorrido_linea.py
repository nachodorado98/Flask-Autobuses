import pytest

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_pagina_recorrido_linea_no_existe(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/recorrido_linea/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_recorrido_linea_existe(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/recorrido_linea/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"Recorrido de la linea {id_linea}" in contenido
	assert "iframe" in contenido
	assert f"/visualizar_mapa_recorrido/mapa_recorrido_linea_{id_linea}.html" in contenido
	assert f"Volver a la linea {id_linea}" in contenido