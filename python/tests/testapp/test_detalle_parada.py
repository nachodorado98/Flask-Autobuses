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

	cliente.post("/insertar_parada", data={"parada":parada})

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

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_pagina_detalle_parada_tiempos_no_existe(cliente, conexion, parada):

	respuesta=cliente.get(f"/detalle_parada/{parada}/tiempos")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada"],
	[(1,),(330,),(356,),(2011,)]
)
def test_pagina_detalle_parada_tiempos_existe_no_es_favorita(cliente, conexion, parada):

	respuesta=cliente.get(f"/detalle_parada/{parada}/tiempos")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "Redirecting..." in contenido

def test_pagina_detalle_parada_tiempos_existe_es_favorita_credenciales_error(cliente_erroneo, conexion):

	cliente_erroneo.post("/insertar_parada", data={"parada":356})

	respuesta=cliente_erroneo.get("/detalle_parada/356/tiempos")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/detalle_parada/356"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada"],
	[(70,),(77,),(69,),(76,)]
)
def test_pagina_detalle_parada_tiempos(cliente, conexion, parada):

	cliente.post("/insertar_parada", data={"parada":parada})

	respuesta=cliente.get(f"/detalle_parada/{parada}/tiempos")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Tiempos de la parada" in contenido
	assert f"{parada}" in contenido
	assert "Actualizar tiempos" in contenido
	assert f"Volver a la parada {parada}" in contenido