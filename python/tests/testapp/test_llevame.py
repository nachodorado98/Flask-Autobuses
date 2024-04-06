import pytest

def test_pagina_llevame(cliente, conexion):

	respuesta=cliente.get("/llevame")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Llevame</h1>" in contenido
	assert "Parada de Origen:" in contenido
	assert "Parada de Destino:" in contenido
	assert "Salir a las:" in contenido

@pytest.mark.parametrize(["parada1", "parada2"],
	[(1,"a"),(None, 356),(2011,"a356"),("1","2011O"),(1,1),("356","356")]
)
def test_pagina_ruta_paradas_error(cliente, conexion, parada1, parada2):

	respuesta=cliente.post("/llevame/ruta",
							data={"parada-origen":parada1, "parada-destino":parada2, "hora":"22:00"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/llevame"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["hora"],
	[(2230,),("22:001",),("222:00",),("22:60",),("24:00",),("24:60",),("-1:00",)]
)
def test_pagina_ruta_hora_error(cliente, conexion, hora):

	respuesta=cliente.post("/llevame/ruta",
							data={"parada-origen":"1", "parada-destino":"2", "hora":hora})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/llevame"
	assert "Redirecting..." in contenido

@pytest.mark.parametrize(["parada1", "parada2"],
	[(1,0),(0,1),(10,356),(356,10),(2010,10),(-9,70)]
)
def test_pagina_ruta_paradas_no_existen(cliente, conexion, parada1, parada2):

	respuesta=cliente.post("/llevame/ruta",
							data={"parada-origen":parada1, "parada-destino":parada2, "hora":"22:00"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/llevame"
	assert "Redirecting..." in contenido

def test_pagina_ruta_credenciales_error(cliente_erroneo, conexion):

	respuesta=cliente_erroneo.post("/llevame/ruta",
									data={"parada-origen":1, "parada-destino":2, "hora":"22:00"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/llevame"
	assert "Redirecting..." in contenido

def test_pagina_ruta(cliente, conexion):

	respuesta=cliente.post("/llevame/ruta",
							data={"parada-origen":1, "parada-destino":2, "hora":"22:00"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Ruta desde Av. de Valdemarin, 88 hasta Av. de Valdemarin, 122" in contenido
	assert "Hora de salida:" in contenido
	assert "Hora de llegada:" in contenido
	assert "Distancia:" in contenido
	assert "Duración:" in contenido
	assert "iframe" in contenido
	assert "Ver Ruta en Detalle" in contenido
	assert "Pasos a seguir" in contenido