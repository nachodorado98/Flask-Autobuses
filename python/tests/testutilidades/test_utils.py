import os
import pytest
from datetime import datetime
from shapely.geometry import Point, LineString

from src.utilidades.utils import crearCarpeta, eliminarPosiblesMapasFolium, leerGeoJSON, crearMapaFolium
from src.utilidades.utils import crearMapaFoliumRecorrido, obtenerToken, obtenerDataAPI, tiempos_lineas_minutos
from src.utilidades.utils import agruparTiemposLinea, limpiarData, obtenerTiemposParada, hora_actual
from src.utilidades.utils import obtenerDataParadaAPI, limpiarDataParada, obtenerDatosParada, paradas_validas
from src.utilidades.utils import hora_valida, obtenerHoraMinutos, obtenerHoy, obtenerDataRecorridoAPI
from src.utilidades.utils import convertirStringDatetime, limpiarDataBasicaRecorrido, limpiarNumeroTramo
from src.utilidades.utils import limpiarDatosBasicosTramo, limpiarPuntoTramo, limpiarLineaTramo, unirDatosTramo
from src.utilidades.utils import limpiarDatosTramo, limpiarDataDetalleRecorrido, limpiarDataRecorrido, obtenerDatosRecorrido
from src.utilidades.utils import crearMapaFoliumRuta, obtenerPasosDetalleRuta

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

@pytest.mark.parametrize(["parada1", "parada2"],
	[(1,"a"),(None, 356),(2011,"a356"),("1a","2011"),(1,1),("356","356")]
)
def test_paradas_validas_no_validas(parada1, parada2):

	assert not paradas_validas(parada1, parada2)

@pytest.mark.parametrize(["parada1", "parada2"],
	[(1,2011),(70, 356),("2011", 356),(2011, "356"),("2011", "356")]
)
def test_paradas_validas(parada1, parada2):

	assert paradas_validas(parada1, parada2)

@pytest.mark.parametrize(["hora"],
	[(2230,),("22:001",),("222:00",),("22:60",),("24:00",),("24:60",),("-1:00",)]
)
def test_hora_valida_no_valida(hora):

	assert not hora_valida(hora)

@pytest.mark.parametrize(["hora"],
	[("22:01",),("00:00",),("23:59",),("13:07",)]
)
def test_hora_valida(hora):

	assert hora_valida(hora)

@pytest.mark.parametrize(["hora", "hora_minutos"],
	[("22:01",(22,1)),("00:00",(0,0)),("23:59",(23,59)),("13:07",(13,7))]
)
def test_obtener_hora_minuos(hora, hora_minutos):

	assert obtenerHoraMinutos(hora)==(hora_minutos)

def test_obtener_hoy():

	hoy=obtenerHoy()

	hoy_datetime=datetime.now()

	assert hoy[0]==hoy_datetime.day
	assert hoy[1]==hoy_datetime.month
	assert hoy[2]==hoy_datetime.year

@pytest.mark.parametrize(["token"],
	[("a",),("",),("token",),("gghghhgghwljsdjkf",)]
)
def test_obtener_data_recorrido_api_token_error(token):

	assert obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22) is None

@pytest.mark.parametrize(["latitud1", "longitud1","latitud2", "longitud2"],
	[
		(0, -3.68, 40.37, -3.75),
		(40.42, 0, 40.37, -3.75),
		(40.42, -3.68, 0, -3.75),
		(40.42, -3.68, 40.37, 0),
		(44.42, -3.68, 40.37, -3.75),
		(40.42, -3.68, 40.37, -1.75)
	]
)
def test_obtener_data_recorrido_api_token_correcto_coordenadas_error(app, latitud1, longitud1, latitud2, longitud2):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	assert obtenerDataRecorridoAPI(token, latitud1, longitud1, "Parada1", latitud2, longitud2, "Parada2", 21, 22) is None

def test_obtener_data_recorrido_api_token_correcto_coordenadas_correctas(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	assert data is not None
	assert data["code"]=="00"
	assert "data" in data.keys()

@pytest.mark.parametrize(["fecha_string"],
	[("ghgghhgj",),("2024-01-11",),("12/03/2024 11:11",)]
)
def test_convertir_string_datetime_error_formato(fecha_string):

	assert convertirStringDatetime(fecha_string)==datetime.now()

@pytest.mark.parametrize(["fecha_string", "ano", "mes", "dia", "horas", "minutos", "segundos"],
	[
		("31/03/2024 17:48:51",2024,3,31,17,48,51),
		("22/06/2024 17:00:51",2024,6,22,17,0,51),
		("13/04/2019 00:48:01",2019,4,13,0,48,1)
	]
)
def test_convertir_string_datetime(fecha_string, ano, mes, dia, horas, minutos, segundos):

	valor_datetime=convertirStringDatetime(fecha_string)

	assert valor_datetime!=datetime.now()
	assert valor_datetime.year==ano
	assert valor_datetime.month==mes
	assert valor_datetime.day==dia
	assert valor_datetime.hour==horas
	assert valor_datetime.minute==minutos
	assert valor_datetime.second==segundos

def test_limpiar_data_basica_recorrido_sin_data():

	assert limpiarDataBasicaRecorrido({"data":[]}) is None

def test_limpiar_data_basica_recorrido_con_data(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	datos_limpios=limpiarDataBasicaRecorrido(data)

	assert datos_limpios is not None
	assert isinstance(datos_limpios, dict)

	for clave in datos_limpios.keys():

		assert clave in ("descripcion", "salida", "llegada", "duracion", "distancia")

@pytest.mark.parametrize(["tramo", "numero"],
	[
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468}, 3),
		({'order': 2,'type': 'Bus','duration': 8.4,'distance': 1.64042,'idLine': '53'}, 2),
		({'order': 5,'type': 'Walk','duration': 2.0,'distance': 0.0673}, 5),
		({'order': 4,'type': 'Bus','duration': 37.1,'distance': 7.90453,'idLine': '34'}, 4)
	]
)
def test_limpiar_numero_tramo(tramo, numero):

	assert limpiarNumeroTramo(tramo)==numero

@pytest.mark.parametrize(["tramo", "tipo","linea"],
	[
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468}, "Andando", "-"),
		({'order': 2,'type': 'Bus','duration': 8.4,'distance': 1.64042,'idLine': '53'}, "Bus", "53"),
		({'order': 5,'type': 'Walk','duration': 2.0,'distance': 0.0673}, "Andando", "-"),
		({'order': 4,'type': 'Bus','duration': 37.1,'distance': 7.90453,'idLine': '34'}, "Bus", "34")
	]
)
def test_limpiar_datos_basicos_tramo(tramo, tipo, linea):

	datos_tramos=limpiarDatosBasicosTramo(tramo)

	assert datos_tramos["tipo"]==tipo
	assert datos_tramos["linea"]==linea
	assert isinstance(datos_tramos["duracion"], int)
	assert isinstance(datos_tramos["distancia"], float)

@pytest.mark.parametrize(["punto_tramo", "parada", "duracion", "distancia"],
	[
		({'type':'Feature','geometry':{'type':'Point','coordinates':[-3.68, 40.42]},
		'properties':{'name':'Goya-Príncipe','description':"En la parada",'idStop':'675'}},"675",None,None),
		({'type':'Feature','geometry':{'type':'Point','coordinates':[-3.69, 40.41]},
		'properties':{'name':'Cibeles','description':'Desciende parada Nº 69','idStop':'69'}}, "69",None,None),
		({'type':'Feature','geometry':{'type':'Point','coordinates':[-3.68, 40.42]},
		'properties':{'description':'Vergara','duration': 1.9781,'distance': 0.38573,'idStop': '675'}}, "675",1,0.4),
		({'type':'Feature','geometry':{'type':'Point','coordinates':[-3.69, 40.41]},
		'properties': {'name':'Cibeles','description': 'Dirígete  Nº 74 (Cibeles).'}}, None, None, None)
	]
)
def test_limpiar_punto_tramo(punto_tramo, parada, duracion, distancia):

	datos_punto=limpiarPuntoTramo(punto_tramo)

	assert isinstance(datos_punto["punto"], Point)
	assert datos_punto["parada"]==parada
	assert datos_punto["duracion"]==duracion
	assert datos_punto["distancia"]==distancia

@pytest.mark.parametrize(["linea_tramo"],
	[
		({'type':'LineString',
			'coordinates':[[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42]]},),
		({'type':'LineString',
			'coordinates':[[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42]]},),
		({'type':'LineString',
			'coordinates':[[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42]]},),
		({'type':'LineString',
			'coordinates':[[-3.68, 40.42],[-3.68, 40.42],[-3.68, 40.42],]},)
	]
)
def test_limpiar_linea_tramo(linea_tramo):

	datos_linea=limpiarLineaTramo(linea_tramo)

	assert isinstance(datos_linea["linea"], LineString)

@pytest.mark.parametrize(["basico", "origen", "destino", "ruta", "itinerario"],
	[
		({"b":"","b1":""},{"o":""},{"d":"","d1":"","d2":""},{"r":"","r1":""},{"i":"","i1":""}),
		({"b":""},{"o":""},{"d":"","d1":"",},{"r":"","r1":""},{"i":"","i1":""}),
		({"b":"","b1":""},{"o":""},{"d":"","d2":""},{"r":"","r1":""},{"i":"","i1":""})
	]
)
def test_unir_datos_tramo(basico, origen, destino, ruta, itinerario):

	datos_unidos=unirDatosTramo(basico, origen, destino, ruta, itinerario)

	basico.update(origen)
	basico.update(destino)
	basico.update(ruta)
	basico.update(itinerario)

	assert len(basico.keys())==len(datos_unidos.keys())

@pytest.mark.parametrize(["tramo"],
	[
		({},),
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468},),
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468, "source":""},),
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468, "destination":"a"},),
		({'order': 3,'type': 'Walk','duration': 1.4,'distance': 0.08468, "route":[{"hola":"adios"}]},),
		({'order': 3,'itinerary': 'Walk','duration': 1.4,'distance': 0.08468},),
	]
)
def test_limpiar_datos_tramo_datos_error(tramo):

	assert not limpiarDatosTramo(tramo)

def test_limpiar_datos_tramo(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	tramo=data["data"]["sections"][0]

	tramo_limpio=limpiarDatosTramo(tramo)

	claves_tramo=tramo_limpio.keys()

	assert "origen" in claves_tramo
	assert "destino" in claves_tramo
	assert "ruta" in claves_tramo
	assert "itinerario" in claves_tramo

def test_limpiar_data_detalle_recorrido_sin_data():

	assert limpiarDataDetalleRecorrido({"data":[]}) is None

def test_limpiar_data_detalle_recorrido_con_data(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	data_limpia=limpiarDataDetalleRecorrido(data)

	tramos=len(data["data"]["sections"])

	assert len(data_limpia)==tramos

def test_limpiar_data_recorrido_sin_data():

	datos=limpiarDataRecorrido({"data":[]})

	assert datos["basico"] is None
	assert datos["detalle"] is None

def test_limpiar_data_recorrido_con_data(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	token=obtenerToken(correo, contrasena)

	data=obtenerDataRecorridoAPI(token, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	datos=limpiarDataRecorrido(data)

	assert datos["basico"] is not None
	assert datos["detalle"] is not None

@pytest.mark.parametrize(["correo", "contrasena"],
	[
		("correo", "contrasena"),
		("nacho", "1234"),
		("nachogolden@gmail.com", "NACHO&ruiz98"),
		("","")
	]
)
def test_obtener_recorrido_error_credenciales(correo, contrasena):

	assert obtenerDatosRecorrido(correo, contrasena, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22) is None

@pytest.mark.parametrize(["latitud1", "longitud1","latitud2", "longitud2"],
	[
		(0, -3.68, 40.37, -3.75),
		(40.42, 0, 40.37, -3.75),
		(40.42, -3.68, 0, -3.75),
		(40.42, -3.68, 40.37, 0),
		(44.42, -3.68, 40.37, -3.75),
		(40.42, -3.68, 40.37, -1.75)
	]
)
def test_obtener_recorrido_error_coordenadas(app, latitud1, longitud1, latitud2, longitud2):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	assert obtenerDatosRecorrido(correo, contrasena, latitud1, longitud1, "Parada1", latitud2, longitud2, "Parada2", 21, 22) is None

def test_obtener_recorrido(app):

	correo=app.config.get("CORREO")
	contrasena=app.config.get("CONTRASENA")

	datos=obtenerDatosRecorrido(correo, contrasena, 40.42, -3.68, "Parada1", 40.37, -3.75, "Parada2", 21, 22)

	assert datos is not None
	assert isinstance(datos, dict)
	assert isinstance(datos["basico"], dict)
	assert isinstance(datos["detalle"], dict)

@pytest.mark.parametrize(["puntos_ruta", "valores_puntos"],
	[
		([Point(-3.1, 40.3)], ["[40.3, -3.1]"]),
		([Point(-3.1, 40.3), Point(-3.1, 40.3)], ["[40.3, -3.1]", "[40.3, -3.1]"]),
		([Point(-3.1, 40.3), Point(-3.5, 40.5)], ["[40.3, -3.1]", "[40.5, -3.5]"])
	]
)
def test_crear_mapa_ruta_bus_ruta_corta(puntos_ruta, valores_puntos):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_ruta")

	ruta_html=os.path.join(ruta_templates, "mapa_ruta.html")

	assert not os.path.exists(ruta_html)

	tramos={1:{'tipo':'Bus',
			'duracion': 4,
			'distancia': 0.3,
			'linea': '-',
			'origen':{'punto': Point(-3.783, 40.47),'nombre':'Av.','descripcion':'Desde Av'},
			'destino':{'punto': Point(-3.786, 40.469),'nombre': 'Av. de Val', 'descripcion':'Hasta Av'},
			'ruta': [{'punto': punto_ruta, 'nombre': '', 'descripcion': 'Avance',} for punto_ruta in puntos_ruta],
			'itinerario': {'linea': LineString([(-3.99, 40.47), (-3.783, 40.51), (-3.7, 40.45)])}}}

	crearMapaFoliumRuta(ruta_relativa, tramos)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert "[40.47, -3.783]" in contenido
		assert "[40.469, -3.786]" in contenido

		for valor in valores_puntos:

			assert valor not in contenido

		assert "[-3.99, 40.47]" in contenido
		assert "[-3.783, 40.51]" in contenido
		assert "[-3.7, 40.45]" in contenido
		
	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

@pytest.mark.parametrize(["puntos_ruta", "valores_puntos_no", "valores_puntos_si"],
	[
		([Point(-3.1, 40.3), Point(-3.2, 40.3), Point(-3.1, 40.3)], ["[40.3, -3.1]", "[40.3, -3.1]"], ["[40.3, -3.2]"]),
		([Point(-3.1, 40.3), Point(-3.2, 40.3), Point(-3.3, 40.9), Point(-3.2, 40.8)], ["[40.3, -3.1]", "[40.8, -3.2]"], ["[40.3, -3.2]", "[40.9, -3.3]"])
	]
)
def test_crear_mapa_ruta_bus_ruta_larga(puntos_ruta, valores_puntos_no, valores_puntos_si):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_ruta")

	ruta_html=os.path.join(ruta_templates, "mapa_ruta.html")

	assert not os.path.exists(ruta_html)

	tramos={1:{'tipo':'Bus',
			'duracion': 4,
			'distancia': 0.3,
			'linea': '-',
			'origen':{'punto': Point(-3.783, 40.47),'nombre':'Av.','descripcion':'Desde Av'},
			'destino':{'punto': Point(-3.786, 40.469),'nombre': 'Av. de Val', 'descripcion':'Hasta Av'},
			'ruta': [{'punto': punto_ruta, 'nombre': '', 'descripcion': 'Avance',} for punto_ruta in puntos_ruta],
			'itinerario': {'linea': LineString([(-3.99, 40.47), (-3.783, 40.51), (-3.7, 40.45)])}}}

	crearMapaFoliumRuta(ruta_relativa, tramos)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		print(contenido)

		assert "[40.47, -3.783]" in contenido
		assert "[40.469, -3.786]" in contenido

		for valor in valores_puntos_no:

			assert valor not in contenido

		for valor in valores_puntos_si:

			assert valor in contenido

		assert "[-3.99, 40.47]" in contenido
		assert "[-3.783, 40.51]" in contenido
		assert "[-3.7, 40.45]" in contenido
		
	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

@pytest.mark.parametrize(["puntos_ruta", "valores_puntos"],
	[
		([Point(-3.1, 40.3)], ["[40.3, -3.1]"]),
		([Point(-3.1, 40.3), Point(-3.1, 40.3)], ["[40.3, -3.1]", "[40.3, -3.1]"]),
		([Point(-3.1, 40.3), Point(-3.5, 40.5)], ["[40.3, -3.1]", "[40.5, -3.5]"])
	]
)
def test_crear_mapa_ruta_andando_ruta_corta(puntos_ruta, valores_puntos):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_ruta")

	ruta_html=os.path.join(ruta_templates, "mapa_ruta.html")

	assert not os.path.exists(ruta_html)

	tramos={1:{'tipo':'Andando',
			'duracion': 4,
			'distancia': 0.3,
			'linea': '-',
			'origen':{'punto': Point(-3.783, 40.47),'nombre':'Av.','descripcion':'Desde Av'},
			'destino':{'punto': Point(-3.786, 40.469),'nombre': 'Av. de Val', 'descripcion':'Hasta Av'},
			'ruta': [{'punto': punto_ruta, 'nombre': '', 'descripcion': 'Avance',} for punto_ruta in puntos_ruta],
			'itinerario': {'linea': LineString([(-3.99, 40.47), (-3.783, 40.51), (-3.7, 40.45)])}}}

	crearMapaFoliumRuta(ruta_relativa, tramos)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert "[40.47, -3.783]" in contenido
		assert "[40.469, -3.786]" in contenido

		for valor in valores_puntos:

			assert valor not in contenido

		assert "[-3.99, 40.47]" not in contenido
		assert "[-3.783, 40.51]" not in contenido
		assert "[-3.7, 40.45]" not in contenido
		
	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

@pytest.mark.parametrize(["puntos_ruta", "valores_puntos_no", "valores_puntos_si"],
	[
		([Point(-3.1, 40.3), Point(-3.2, 40.3), Point(-3.1, 40.3)], ["[40.3, -3.1]", "[40.3, -3.1]"], ["[40.3, -3.2]"]),
		([Point(-3.1, 40.3), Point(-3.2, 40.3), Point(-3.3, 40.9), Point(-3.2, 40.8)], ["[40.3, -3.1]", "[40.8, -3.2]"], ["[40.3, -3.2]", "[40.9, -3.3]"])
	]
)
def test_crear_mapa_ruta_andando_ruta_larga(puntos_ruta, valores_puntos_no, valores_puntos_si):

	ruta_relativa=os.path.join(os.path.abspath(".."), "src")

	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

	ruta_templates=os.path.join(ruta_relativa, "templates", "templates_mapas_ruta")

	ruta_html=os.path.join(ruta_templates, "mapa_ruta.html")

	assert not os.path.exists(ruta_html)

	tramos={1:{'tipo':'Andando',
			'duracion': 4,
			'distancia': 0.3,
			'linea': '-',
			'origen':{'punto': Point(-3.783, 40.47),'nombre':'Av.','descripcion':'Desde Av'},
			'destino':{'punto': Point(-3.786, 40.469),'nombre': 'Av. de Val', 'descripcion':'Hasta Av'},
			'ruta': [{'punto': punto_ruta, 'nombre': '', 'descripcion': 'Avance',} for punto_ruta in puntos_ruta],
			'itinerario': {'linea': LineString([(-3.99, 40.47), (-3.783, 40.51), (-3.7, 40.45)])}}}

	crearMapaFoliumRuta(ruta_relativa, tramos)

	assert os.path.exists(ruta_html)

	with open(ruta_html, "r") as html:

		contenido=html.read()

		assert "[40.47, -3.783]" in contenido
		assert "[40.469, -3.786]" in contenido

		for valor in valores_puntos_no:

			assert valor not in contenido

		for valor in valores_puntos_si:

			assert valor not in contenido

		assert "[-3.99, 40.47]" not in contenido
		assert "[-3.783, 40.51]" not in contenido
		assert "[-3.7, 40.45]" not in contenido
		
	eliminarPosiblesMapasFolium(ruta_relativa, "templates_mapas_ruta", "mapa_ruta")

@pytest.mark.parametrize(["numero_tramos"],
	[(1,),(4,),(3,),(7,),(22,),(13,)]
)
def test_obtener_pasos_detalle_ruta(numero_tramos):

	tramo={'tipo':'Andando','origen':{'descripcion':'Desde Av'},'destino':{'descripcion':'Hasta Av'},'ruta':[],'itinerario':{}}

	tramos={numero:tramo for numero in range(1, numero_tramos+1)}

	datos_pasos=obtenerPasosDetalleRuta(tramos)

	assert len(datos_pasos)==numero_tramos

	for valor in ["tipo", "origen-destino"]:

		for numero_paso, datos_paso in datos_pasos.items():

			assert valor in list(datos_paso.keys())