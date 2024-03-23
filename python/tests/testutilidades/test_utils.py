import os
import pytest

from src.utilidades.utils import crearCarpeta, eliminarPosiblesMapasFolium, leerGeoJSON, crearMapaFolium

def borrarCarpeta(ruta):

	if os.path.exists(ruta):

		os.rmdir(ruta)

def test_crear_carpeta_no_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert not os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

def test_crear_carpeta_existe():

	ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

	assert os.path.exists(ruta_carpeta)

	crearCarpeta(ruta_carpeta)

	assert os.path.exists(ruta_carpeta)

	borrarCarpeta(ruta_carpeta)

#  Funcion complementaria para crear el HTML del geojson
def crearHTML(ruta_html:str)->None:

	contenido="""
			<!DOCTYPE html>
			<html>
			<head>
			    <title>Mi Archivo HTML</title>
			</head>
			<body>
			    <h1>Hola, este es mi archivo HTML creado con Python</h1>
			</body>
			</html>
			"""

	with open(ruta_html, "w") as html:

	    html.write(contenido)

def test_eliminar_posibles_mapa_folium_existe():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_paradas")

	ruta_html=os.path.join(ruta_templates, "mapa_parada1.html")

	crearHTML(ruta_html)

	archivos_antes=len(os.listdir(ruta_templates))

	eliminarPosiblesMapasFolium(ruta_relativa)

	archivos_despues=len(os.listdir(ruta_templates))

	assert archivos_antes!=archivos_despues
	assert archivos_antes>archivos_despues
	assert archivos_antes-1==archivos_despues

def test_eliminar_posibles_mapa_folium_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_paradas")

	for numero in range(5):

		ruta_html=os.path.join(ruta_templates, f"mapa_parada{numero}.html")

		crearHTML(ruta_html)

	archivos_antes=len(os.listdir(ruta_templates))

	eliminarPosiblesMapasFolium(ruta_relativa)

	archivos_despues=len(os.listdir(ruta_templates))

	assert archivos_antes!=archivos_despues
	assert archivos_antes>archivos_despues
	assert archivos_antes-5==archivos_despues

def test_leer_geojson_barrios_no_existen():

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	assert leerGeoJSON(ruta_relativa, []).empty

@pytest.mark.parametrize(["barrio"],
	[("prosperidad",), ("Aeropuert",), ("BuenaVISTA",)]
)
def test_leer_geojson_barrios_existe_error(barrio):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	assert leerGeoJSON(ruta_relativa, [barrio]).empty

@pytest.mark.parametrize(["barrio"],
	[("Prosperidad",), ("Aeropuerto",), ("Buenavista",)]
)
def test_leer_geojson_barrios_existe(barrio):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	geodataframe=leerGeoJSON(ruta_relativa, [barrio])

	assert not geodataframe.empty
	assert len(geodataframe)==1

@pytest.mark.parametrize(["barrios", "resultado"],
	[
		(["Prosperidad", "Aeropuerto", "Buenavista"], 3),
		(["Prosperidad", "Buenavista"], 2),
		(["Prosperidad", "Aeropuerto", "Buenavista", "Prosperidad"], 3),
		(["Prosperidad", "Prosperidad", "Prosperidad"], 1),
		(["Prosperidad", "Aeropuerto", "BuenavistA"], 2)
	]
)
def test_leer_geojson_barrios_existen(barrios, resultado):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	geodataframe=leerGeoJSON(ruta_relativa, barrios)

	assert not geodataframe.empty
	assert len(geodataframe)==resultado

@pytest.mark.parametrize(["parada", "numero"],
	[
		("Cibeles", 70),
		("Casa", 2011),
		("Amanda", 356)
	]
)
def test_crear_mapa_barrio_no_existen_parada_existe(parada, numero):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_paradas")

	ruta_html=os.path.join(ruta_templates, "mapa_parada.html")

	assert not os.path.exists(ruta_html)

	crearMapaFolium(ruta_relativa, [], {"latitud":40, "longitud":-3, "parada":parada, "numero_parada":numero})

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada in contenido
		assert f"Parada {numero}" in contenido

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["parada", "numero", "barrio"],
	[
		("Cibeles", 70, "Prosperidad"),
		("Casa", 2011, "Buenavista"),
		("Amanda", 356, "Aeropuerto")
	]
)
def test_crear_mapa_barrio_existe_parada_existe(parada, numero, barrio):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_paradas")

	ruta_html=os.path.join(ruta_templates, "mapa_parada.html")

	assert not os.path.exists(ruta_html)

	crearMapaFolium(ruta_relativa, [barrio], {"latitud":40, "longitud":-3, "parada":parada, "numero_parada":numero})

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada in contenido
		assert f"Parada {numero}" in contenido
		assert barrio in contenido

	eliminarPosiblesMapasFolium(ruta_relativa)

@pytest.mark.parametrize(["parada", "numero", "barrios"],
	[
		("Cibeles", 70, ["Prosperidad", "Aeropuerto", "Buenavista"]),
		("Casa", 2011, ["Prosperidad", "Buenavista"]),
		("Amanda", 356, ["Prosperidad", "Aeropuerto"])
	]
)
def test_crear_mapa_barrio_existen_parada_existe(parada, numero, barrios):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa)

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_paradas")

	ruta_html=os.path.join(ruta_templates, "mapa_parada.html")

	assert not os.path.exists(ruta_html)

	crearMapaFolium(ruta_relativa, barrios, {"latitud":40, "longitud":-3, "parada":parada, "numero_parada":numero})

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada in contenido
		assert f"Parada {numero}" in contenido

		for barrio in barrios:

			assert barrio in contenido

	eliminarPosiblesMapasFolium(ruta_relativa)