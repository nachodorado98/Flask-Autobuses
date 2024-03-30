import pytest

def test_pagina_llevame(cliente, conexion):

	respuesta=cliente.get("/llevame")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Llevame</h1>" in contenido
	assert "Parada de Origen:" in contenido
	assert "Parada de Destino:" in contenido
	assert "Salir a las:" in contenido