import pytest

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_pagina_detalle_parada_no_existe(cliente, conexion, parada):

	respuesta=cliente.get(f"/detalle_parada/{parada}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada"],
	[(1,),(330,),(356,),(2011,)]
)
def test_pagina_detalle_parada_existe_no_es_favorita(cliente, conexion, parada):

	respuesta=cliente.get(f"/detalle_parada/{parada}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada"],
	[(1,),(330,),(356,),(2011,)]
)
def test_pagina_detalle_parada_existe_es_favorita(cliente, conexion, parada):

	cliente.post(f"/insertar_parada", data={"parada":parada})

	respuesta=cliente.get(f"/detalle_parada/{parada}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert f"<h1>Detalle de la Parada Nº {parada}</h1>" in contenido
	assert "Barrio de" in contenido
	assert "Distrito" in contenido
	assert "(MADRID)" in contenido
	assert "iframe" in contenido
	assert f"/visualizar_mapa_parada/mapa_parada_{parada}.html" in contenido
	assert "Volver" in contenido