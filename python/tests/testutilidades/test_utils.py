import os
import pytest

from src.utilidades.utils import crearCarpeta, eliminarPosiblesMapasFolium, leerGeoJSON, crearMapaFolium
from src.utilidades.utils import crearMapaFoliumRecorrido, obtenerToken, obtenerDataAPI, tiempos_lineas_minutos
from src.utilidades.utils import agruparTiemposLinea, limpiarData, obtenerTiemposParada, hora_actual
from src.utilidades.utils import obtenerDataParadaAPI, limpiarDataParada, obtenerDatosParada

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

@pytest.mark.parametrize(["parada1", "numero1", "parada2", "numero2"],
	[
		("Cibeles", 70, "Casa", 22),
		("Casa", 2011, "Amanda", 13),
		("Amanda", 356, "Cibeles", 22)
	]
)
def test_crear_mapa_recorrido_barrio_no_existen_paradas_existen(numero1, parada1, numero2, parada2):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_recorrido")

	ruta_html=os.path.join(ruta_templates, "mapa_recorrido_linea.html")

	assert not os.path.exists(ruta_html)

	crearMapaFoliumRecorrido(ruta_relativa, [], [(numero1, parada1, 40, -3)], [(numero2, parada2, 40, -3)])

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada1 in contenido
		assert parada2 in contenido
		assert f"Parada {numero1}" in contenido
		assert f"Parada {numero2}" in contenido

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

@pytest.mark.parametrize(["parada1", "numero1", "parada2", "numero2", "barrio"],
	[
		("Cibeles", 70, "Casa", 22, "Prosperidad"),
		("Casa", 2011, "Amanda", 13, "Buenavista"),
		("Amanda", 356, "Cibeles", 22, "Aeropuerto")
	]
)
def test_crear_mapa_recorrido_barrio_existe_paradas_existen(numero1, parada1, numero2, parada2, barrio):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_recorrido")

	ruta_html=os.path.join(ruta_templates, "mapa_recorrido_linea.html")

	assert not os.path.exists(ruta_html)

	crearMapaFoliumRecorrido(ruta_relativa, [barrio], [(numero1, parada1, 40, -3)], [(numero2, parada2, 40, -3)])

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada1 in contenido
		assert parada2 in contenido
		assert f"Parada {numero1}" in contenido
		assert f"Parada {numero2}" in contenido
		assert barrio in contenido

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

@pytest.mark.parametrize(["parada1", "numero1", "parada2", "numero2", "barrios"],
	[
		("Cibeles", 70, "Casa", 22, ["Prosperidad", "Aeropuerto", "Buenavista"]),
		("Casa", 2011, "Amanda", 13, ["Prosperidad", "Buenavista"]),
		("Amanda", 356, "Cibeles", 22, ["Prosperidad", "Aeropuerto"])
	]
)
def test_crear_mapa_recorrido_barrio_existen_paradas_existen(numero1, parada1, numero2, parada2, barrios):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_recorrido")

	ruta_html=os.path.join(ruta_templates, "mapa_recorrido_linea.html")

	assert not os.path.exists(ruta_html)

	crearMapaFoliumRecorrido(ruta_relativa, barrios, [(numero1, parada1, 40, -3)], [(numero2, parada2, 40, -3)])

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert parada1 in contenido
		assert parada2 in contenido
		assert f"Parada {numero1}" in contenido
		assert f"Parada {numero2}" in contenido
		
		for barrio in barrios:

			assert barrio in contenido

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_recorrido", "mapa_recorrido_linea")

@pytest.mark.parametrize(["correo", "contrasena"],
	[
		("correo", "contrasena"),
		("nacho", "1234"),
		("nachogolden@gmail.com", "NACHO&ruiz98"),
		("","")
	]
)
def test_obtener_token_error_credenciales(correo, contrasena):

	assert obtenerToken(correo, contrasena) is None

@pytest.mark.parametrize(["contrasena"],
	[("contrasena",),("1234",),("NACHO&ruiz98",),("",)]
)
def test_obtener_token_error_contrasena(app, contrasena):

	correo=app.config.get("CORREO")

	assert obtenerToken(correo, contrasena) is None

@pytest.mark.parametrize(["correo"],
	[("correo",),("nacho",),("nachogolden@gmail.com",),("",)]
)
def test_obtener_token_error_correo(app, correo):

	contrasena=app.config.get("CONTRASENA")

	assert obtenerToken(correo, contrasena) is None

def test_obtener_token_credenciales_correctas(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	assert token is not None
	assert isinstance(token, str)

@pytest.mark.parametrize(["token"],
	[("a",),("",),("token",),("gghghhgghwljsdjkf",)]
)
def test_obtener_data_api_token_error(token):

	assert obtenerDataAPI(token, 1) is None

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_obtener_data_api_token_correcto_no_existe_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	assert obtenerDataAPI(token, parada) is None

@pytest.mark.parametrize(["parada"],
	[(70,),(77,),(69,),(76,)]
)
def test_obtener_data_api_token_correcto_existe_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataAPI(token, parada)

	assert data is not None
	assert data["code"]=="00"
	assert "data" in data.keys()

@pytest.mark.parametrize(["segundos", "minutos"],
	[(1,0),(530,8),(56,0),(110,1),(121,2)]
)
def test_tiempos_lineas_minutos(segundos, minutos):

	assert tiempos_lineas_minutos(("34", segundos))==("34", minutos)

@pytest.mark.parametrize(["tiempos", "resultado"],
	[
		([("139", 0),("34", 1),("34", 12),("139", 21)], {"139": [0, 21], "34": [1, 12]}),
		([("1", 0),("34", 1),("34", 12),("139", 21)], {"139": [21], "34": [1, 12], "1":[0]})
	]
)
def test_agrupar_tiempos_lineas(tiempos, resultado):

	assert agruparTiemposLinea(tiempos)==resultado

def test_limpiar_data_sin_data():

	assert limpiarData({"data":[]}) is None

@pytest.mark.parametrize(["parada"],
	[(70,),(77,),(69,),(76,)]
)
def test_limpiar_data_con_data(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataAPI(token, parada)

	datos_limpios=limpiarData(data)

	assert datos_limpios is not None

@pytest.mark.parametrize(["correo", "contrasena"],
	[
		("correo", "contrasena"),
		("nacho", "1234"),
		("nachogolden@gmail.com", "NACHO&ruiz98"),
		("","")
	]
)
def test_obtener_tiempos_parada_error_credenciales(correo, contrasena):

	assert obtenerTiemposParada(correo, contrasena, 356) is None

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_obtener_tiempos_parada_error_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	assert obtenerTiemposParada(correo, contrasena, parada) is None

@pytest.mark.parametrize(["parada"],
	[(70,),(77,),(69,),(76,)]
)
def test_obtener_tiempos_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	tiempos=obtenerTiemposParada(correo, contrasena, parada)

	assert tiempos is not None
	assert isinstance(tiempos, dict)

def test_hora_actual_tupla():

	hora, minuto=hora_actual(string=False)

	assert isinstance(hora, str)
	assert isinstance(minuto, str)

def test_hora_actual_cadena():

	hora_minuto=hora_actual(string=True)

	assert isinstance(hora_minuto, str)

	hora, minuto=hora_actual(string=False)

	assert hora_minuto==f"{hora}:{minuto}"

@pytest.mark.parametrize(["token"],
	[("a",),("",),("token",),("gghghhgghwljsdjkf",)]
)
def test_obtener_data_parada_api_token_error(token):

	assert obtenerDataParadaAPI(token, 1) is None

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_obtener_data_parada_api_token_correcto_no_existe_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	assert obtenerDataParadaAPI(token, parada) is None

@pytest.mark.parametrize(["parada"],
	[(1,),(356,),(2011,),(70,)]
)
def test_obtener_data_parada_api_token_correcto_existe_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataParadaAPI(token, parada)

	assert data is not None
	assert data["code"]=="00"
	assert "data" in data.keys()

def test_limpiar_data_parada_sin_data():

	assert limpiarDataParada({"data":[]}) is None

@pytest.mark.parametrize(["parada"],
	[(1,),(356,),(2011,),(70,)]
)
def test_limpiar_data_parada_con_data(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataParadaAPI(token, parada)

	datos_limpios=limpiarDataParada(data)

	assert datos_limpios is not None
	assert isinstance(datos_limpios, dict)
	assert datos_limpios["latitud"]>datos_limpios["longitud"]

@pytest.mark.parametrize(["correo", "contrasena"],
	[
		("correo", "contrasena"),
		("nacho", "1234"),
		("nachogolden@gmail.com", "NACHO&ruiz98"),
		("","")
	]
)
def test_obtener_datos_parada_error_credenciales(correo, contrasena):

	assert obtenerDatosParada(correo, contrasena, 356) is None

@pytest.mark.parametrize(["parada"],
	[(0,),(10,),(-9,),(12,),(2010,)]
)
def test_obtener_datos_parada_error_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	assert obtenerDatosParada(correo, contrasena, parada) is None

@pytest.mark.parametrize(["parada"],
	[(1,),(356,),(2011,),(70,)]
)
def test_obtener_datos_parada(app, parada):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	datos=obtenerDatosParada(correo, contrasena, parada)

	assert datos is not None
	assert isinstance(datos, dict)
	assert datos["latitud"]>datos["longitud"]