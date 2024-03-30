import os
from typing import List, Dict, Optional, Union
import geopandas as gpd
import folium
import requests
from datetime import datetime

from .confutils import URL_BASE, ENDPOINT_LOGIN, ENDPOINT_PARADAS, ENDPOINT_DETALLE, ENDPOINT_TIEMPOS
from .confutils import ENDPOINT_RUTA

# Funcion para crear una carpeta si no existe 
def crearCarpeta(ruta_carpeta:str)->None:

	if not os.path.exists(ruta_carpeta):

		os.mkdir(ruta_carpeta)

		print("Creando carpeta...")

# Funcion para eliminar los posibles mapas (archivos html) si existen
def eliminarPosiblesMapasFolium(ruta:str, carpeta:str="templates_mapas_paradas", archivo:str="mapa_parada")->None:

	ruta_templates=os.path.join(ruta, "templates", carpeta)

	posibles_mapas=[archivo for archivo in os.listdir(ruta_templates) if archivo.startswith(archivo)]

	for mapa in posibles_mapas:

		os.remove(os.path.join(ruta_templates, mapa))

# Funcion para leer el archivo geojson
def leerGeoJSON(ruta:str, barrios:List[str])->gpd.geodataframe.GeoDataFrame:

	ruta_carpeta=os.path.join(ruta, "static", "geojson")

	archivo_geojson=os.path.join(ruta_carpeta, "gis.geojson")

	geodataframe=gpd.read_file(archivo_geojson)

	geodataframe_barrios=geodataframe[geodataframe["neighbourhood"].isin(barrios)]

	return geodataframe_barrios

# Funcion para crear el mapa con folium y guardarlo en un html
def crearMapaFolium(ruta:str, barrios:List[str], datos_parada:Dict, nombre_html:str="mapa_parada.html")->None:

	geodataframe=leerGeoJSON(ruta, barrios)

	mapa=folium.Map(location=[datos_parada["latitud"], datos_parada["longitud"]], zoom_start=14)
	 
	folium.GeoJson(geodataframe, name="parada").add_to(mapa)

	folium.Marker([datos_parada["latitud"], datos_parada["longitud"]],
					tooltip=f"Parada {datos_parada['numero_parada']}",
					popup=folium.Popup(f"<h3>{datos_parada['parada']}</h3>",
					max_width=500)).add_to(mapa)

	ruta_templates=os.path.join(ruta, "templates", "templates_mapas_paradas")

	ruta_archivo_html=os.path.join(ruta_templates, nombre_html)

	mapa.save(ruta_archivo_html)

# Funcion para crear el mapa con folium y guardarlo en un html
def crearMapaFoliumRecorrido(ruta:str, barrios:List[str], paradas_ida:List[tuple], paradas_vuelta:List[tuple], nombre_html:str="mapa_recorrido_linea.html")->None:

	geodataframe=leerGeoJSON(ruta, barrios)

	mapa=folium.Map(location=[paradas_ida[0][2], paradas_ida[0][3]], zoom_start=13)
	 
	folium.GeoJson(geodataframe, name="recorrido").add_to(mapa)

	for parada_ida in paradas_ida:

		folium.Marker([parada_ida[2], parada_ida[3]],
						tooltip=f"Parada {parada_ida[0]}",
						popup=folium.Popup(f"<h3>{parada_ida[1]}</h3>",
						max_width=500),
						icon=folium.Icon(color="blue")).add_to(mapa)

	for parada_vuelta in paradas_vuelta:

		folium.Marker([parada_vuelta[2], parada_vuelta[3]],
						tooltip=f"Parada {parada_vuelta[0]}",
						popup=folium.Popup(f"<h3>{parada_vuelta[1]}</h3>",
						max_width=500),
						icon=folium.Icon(color="red")).add_to(mapa)

	ruta_templates=os.path.join(ruta, "templates", "templates_mapas_recorrido")

	ruta_archivo_html=os.path.join(ruta_templates, nombre_html)

	mapa.save(ruta_archivo_html)

# Funcion para obtener el token de autenticacion de la API de la EMT
def obtenerToken(correo:str, contrasena:str)->Optional[str]:

	cabecera={"email":correo, "password":contrasena}

	respuesta=requests.get(f"{URL_BASE}{ENDPOINT_LOGIN}", headers=cabecera)

	if respuesta.status_code!=200:

		return None

	data=respuesta.json()

	if data["code"]!="01":

		return None

	return data["data"][0]["accessToken"]

# Funcion para obtener los datos de la API de la EMT
def obtenerDataAPI(token:str, id_parada:int)->Dict:

	cabecera={"accessToken":token}

	cuerpo={"stopId":id_parada, "Text_EstimationsRequired_YN":"Y"}

	respuesta=requests.post(f"{URL_BASE}{ENDPOINT_PARADAS}/{id_parada}{ENDPOINT_TIEMPOS}",
							headers=cabecera,
							json=cuerpo)

	if respuesta.status_code!=200:

		return None

	data=respuesta.json()

	return None if data["code"]!="00" else data

# Funcion para pasar los minutos a segundos
def tiempos_lineas_minutos(datos:tuple)->tuple:

	minutos=int(datos[1]/60)

	return datos[0], minutos

# Funcion para agrupar las lineas con sus tiempos
def agruparTiemposLinea(tiempos:List[tuple])->Dict:

	tiempos_agrupados={}

	for linea, tiempo in tiempos:

		if linea not in tiempos_agrupados:

			tiempos_agrupados[linea]=[tiempo]

		else:

			tiempos_agrupados[linea].append(tiempo)

	return tiempos_agrupados

# Funcion para limpiar los datos de tiempos de la parada
def limpiarData(data:Dict)->Dict:

	if not data["data"]:

		return None

	tiempos_lineas=[(linea["line"], linea["estimateArrive"]) for linea in data["data"][0]["Arrive"]]

	tiempos_lineas=list(map(tiempos_lineas_minutos, tiempos_lineas))

	return agruparTiemposLinea(tiempos_lineas)

# Funcion para obtener los tiempos de una parada
def obtenerTiemposParada(correo:str, contrasena:str, parada:int)->Optional[Dict]:

	try:

		token=obtenerToken(correo, contrasena)

		data=obtenerDataAPI(token, parada)

		return limpiarData(data)

	except Exception:

		return None

# Funcion para obtener la hora actual
def hora_actual(string:bool=True)->Union[str, tuple[str]]:

	hoy=datetime.now()

	hora_formateada=f"{hoy.hour:02d}"
	minuto_formateado=f"{hoy.minute:02d}"

	return (hora_formateada, minuto_formateado) if not string else f"{hora_formateada}:{minuto_formateado}"

# Funcion para obtener datos de la parada de la API EMT
def obtenerDataParadaAPI(token:str, id_parada:int)->Dict:

	cabecera={"accessToken":token}

	respuesta=requests.get(f"{URL_BASE}{ENDPOINT_PARADAS}/{id_parada}{ENDPOINT_DETALLE}",
							headers=cabecera)

	if respuesta.status_code!=200:

		return None

	data=respuesta.json()

	return None if data["code"]!="00" else data

# Funcion para limpiar los datos de la parada
def limpiarDataParada(data:Dict)->Dict:

	if not data["data"]:

		return None

	longitud, latitud=data["data"][0]["stops"][0]["geometry"]["coordinates"]

	direccion=data["data"][0]["stops"][0]["postalAddress"]

	return {"latitud":latitud, "longitud":longitud, "direccion":direccion}

# Funcion para obtener los datos en detalle de una parada
def obtenerDatosParada(correo:str, contrasena:str, parada:int)->Optional[Dict]:

	try:

		token=obtenerToken(correo, contrasena)

		data=obtenerDataParadaAPI(token, parada)

		return limpiarDataParada(data)

	except Exception:

		return None