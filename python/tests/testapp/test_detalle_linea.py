import pytest

@pytest.mark.parametrize(["id_linea"],
	[(0,),(3400,),(-9,),(1392,)]
)
def test_pagina_detalle_linea_no_existe(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/detalle_linea/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["id_linea"],
	[(1,),(34,),(9,),(139,)]
)
def test_pagina_detalle_linea_existe(cliente, conexion, id_linea):

	respuesta=cliente.get(f"/detalle_linea/{id_linea}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"Detalle de la Linea {id_linea}" in contenido
	assert "Autobus" in contenido
	assert f"Numero de paradas de la linea {id_linea}:" in contenido
	assert f"Recorrido Linea {id_linea}" in contenido
	assert "Seleccionar paradas favoritas" in contenido