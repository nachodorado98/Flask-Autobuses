import os
from typing import List, Dict, Optional, Union
import geopandas as gpd
import folium
import requests
from datetime import datetime
from shapely.geometry import Point, LineString

from .confutils import URL_BASE, ENDPOINT_LOGIN, ENDPOINT_PARADAS, ENDPOINT_DETALLE, ENDPOINT_TIEMPOS
from .confutils import ENDPOINT_RUTA, INICIO_MAPA, TIPO_MARKER

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

# Funcion para validar las paradas
def paradas_validas(parada1:int, parada2:int)->bool:

	try:

		parada1_entero=int(parada1)
		parada2_entero=int(parada2)

		return False if parada1_entero==parada2_entero else True

	except Exception:

		return False

# Funcion para validar la hora
def hora_valida(hora:str)->bool:

	try:

		if len(hora)!=5 or hora[2]!=":":

			return False

		horas, minutos=hora.split(":")
		
		horas=int(horas)
		minutos=int(minutos)
		
		return True if 0<=horas<=23 and 0<=minutos<=59 else False

	except Exception:

		return False

# Funcion para separar la hora
def obtenerHoraMinutos(hora:str)->tuple[int]:

	horas, minutos=hora.split(":")

	return int(horas), int(minutos)

# Funcion para obtener la fecha de hoy
def obtenerHoy()->tuple[int]:

	hoy=datetime.now()

	return hoy.day, hoy.month, hoy.year

# Funcion para obtener el recorrido de la API EMT
def obtenerDataRecorridoAPI(token:str,
							latitud1:float,
							longitud1:float,
							direccion1:str,
							latitud2:float,
							longitud2:float,
							direccion2:str,
							hora:int,
							minuto:int)->Dict:
	
	dia, mes, ano=obtenerHoy()

	cabecera={"accessToken":token}

	cuerpo={"routeType":"P","itinerary":True,"coordinateXFrom":longitud1,"coordinateYFrom":latitud1,
			"coordinateXTo":longitud2,"coordinateYTo":latitud2,"originName":direccion1,
			"destinationName":direccion2,"day":dia,"month":mes,"year":ano,"hour":hora,"minute":minuto,
			"culture": "es","allowBus":True,"allowBike":False}

	respuesta=requests.post(f"{URL_BASE}{ENDPOINT_RUTA}",
							headers=cabecera,
							json=cuerpo)

	if respuesta.status_code!=200:

		return None

	data=respuesta.json()

	return None if data["code"]!="00" else data

# Funcion para convertir a datetime una fecha hora dd/mm/yyyy hh:mm:ss
def convertirStringDatetime(fecha_hora:str)->datetime:

	try:

		fecha, hora=fecha_hora.split(" ")

		dia, mes, ano=fecha.split("/")

		horas, minutos, segundos=hora.split(":")

		return datetime(int(ano), int(mes), int(dia), int(horas), int(minutos), int(segundos))

	except Exception:

		return datetime.now()

# Funcion para limpiar los datos basicos del recorrido parada
def limpiarDataBasicaRecorrido(data:Dict)->Dict:

	if not data["data"]:

		return None

	return {"descripcion":data["data"]["description"],
			"salida":convertirStringDatetime(data["data"]["departureTime"]),
			"llegada":convertirStringDatetime(data["data"]["arrivalTime"]),
			"duracion":int(data["data"]["duration"]),
			"distancia":round(data["data"]["distance"],1)}

# Funcion para limpiar el numero del tramo
def limpiarNumeroTramo(tramo:Dict)->int:

	return tramo["order"]

# Funcion para limpiar datos basicos del tramo
def limpiarDatosBasicosTramo(tramo:Dict)->Dict:

	tipo="Andando" if tramo["type"]=="Walk" else tramo["type"]

	linea="-" if tramo["type"]=="Walk" else tramo["idLine"]

	return {"tipo":tipo,
			"duracion":int(tramo["duration"]),
			"distancia":round(tramo["distance"],1),
			"linea":linea}

# Funcion para limpiar un punto del tramo
def limpiarPuntoTramo(punto_tramo:Dict)->Dict:

	punto_coordenadas=punto_tramo["geometry"]["coordinates"]

	objeto_punto=Point(punto_coordenadas)

	nombre=punto_tramo["properties"].get("name")

	descripcion=punto_tramo["properties"].get("description")

	duracion=punto_tramo["properties"].get("duration")

	distancia=punto_tramo["properties"].get("distance")

	return {"punto":objeto_punto,
			"nombre":"" if nombre is None else nombre,
			"descripcion": "" if descripcion is None else descripcion,
			"parada":punto_tramo["properties"].get("idStop"),
			"duracion":None if duracion is None else int(duracion),
			"distancia":None if distancia is None else round(distancia,1)}

# Funcion para limpiar un linea del tramo
def limpiarLineaTramo(linea_tramo:Dict)->Dict:

	linea_coordenadas=linea_tramo["coordinates"]

	return {"linea":LineString(linea_coordenadas)}

# Funcion para unir todos los datos del tramo en un diccionario
def unirDatosTramo(basico:Dict, origen:Dict, destino:Dict, ruta:Dict, itinerario:Dict)->Dict:

	return {**basico, **origen, **destino, **ruta, **itinerario}

# Funcion para limpiar los datos del tramo
def limpiarDatosTramo(tramo:Dict)->Dict:

	try:

		datos_basicos_tramo=limpiarDatosBasicosTramo(tramo)

		punto_origen_tramo={"origen":limpiarPuntoTramo(tramo["source"])}

		punto_destino_tramo={"destino":limpiarPuntoTramo(tramo["destination"])}

		puntos_ruta_tramo={"ruta":list(map(limpiarPuntoTramo, tramo["route"]["features"]))}

		linea_itinerario={"itinerario":limpiarLineaTramo(tramo["itinerary"])}

		datos_unificados_tramo=unirDatosTramo(datos_basicos_tramo,
										punto_origen_tramo,
										punto_destino_tramo,
										puntos_ruta_tramo,
										linea_itinerario)

		return datos_unificados_tramo

	except Exception:

		return {}

# Funcion para limpiar los datos detallados del recorrido
def limpiarDataDetalleRecorrido(data:Dict)->Dict:

	if not data["data"]:

		return None

	return {limpiarNumeroTramo(tramo): limpiarDatosTramo(tramo) for tramo in data["data"]["sections"]}

# Funcion para limpiar los datos totales del recorrido parada
def limpiarDataRecorrido(data:Dict)->Dict:

	return {"basico":limpiarDataBasicaRecorrido(data),
			"detalle":limpiarDataDetalleRecorrido(data)}

# Funcion para obtener los datos del recorrido
def obtenerDatosRecorrido(correo:str,
							contrasena:str,
							latitud1:float,
							longitud1:float,
							direccion1:str,
							latitud2:float,
							longitud2:float,
							direccion2:str,
							hora:int,
							minuto:int)->Optional[Dict]:

	try:

		token=obtenerToken(correo, contrasena)

		data=obtenerDataRecorridoAPI(token,
									latitud1,
									longitud1,
									direccion1,
									latitud2,
									longitud2,
									direccion2,
									hora,
									minuto)

		return limpiarDataRecorrido(data)

	except Exception:

		return None

# Funcion para agregar ua linea al mapa
def agregarLinea(linea:LineString, mapa:folium.Map)->None:

	linea_geojson=folium.GeoJson(linea.__geo_interface__)

	linea_geojson.add_to(mapa)

# Funcion para obtener la imagen que poner en el marker
def obtenerHTMLMarker(tipo:str, circulo:bool=False)->str:

	if circulo:

		return """<div style="width: 20px;
		            height: 20px;
		            background-color: blue;
		            border-radius: 50%;
		            border: 1px solid white;">
				</div>"""
	else:

		return f"""<div style="background-color: {TIPO_MARKER[tipo]["color"]};
		            color: white;
		            width: {TIPO_MARKER[tipo]["dimension"]}px;
		            height: {TIPO_MARKER[tipo]["dimension"]}px;
		            line-height: 30px;
		            text-align: center;">
			        <i class="fas fa-{TIPO_MARKER[tipo]["icono"]}"></i>
			    </div>"""

# Funcion para agregar un punto (marker) al mapa
def agregarPuntoMarker(latitud:float, longitud:float, tooltip:str, descripcion:str, tipo:str, coordenadas_agregadas:List, mapa:folium.Map, circulo:bool=False)->None:

	if [latitud, longitud] in coordenadas_agregadas:

		latitud+=0.0001
		longitud+=0.0001

	coordenadas_agregadas.append([latitud, longitud])

	folium.Marker([latitud, longitud],
					tooltip=None if circulo else tooltip,
					popup=folium.Popup(descripcion, max_width=10),
					icon=folium.DivIcon(html=obtenerHTMLMarker(tipo, circulo))).add_to(mapa)

# Funcion para crear el mapa de la ruta con folium y guardarlo en un html
def crearMapaFoliumRuta(ruta:str, tramos:Dict, nombre_html:str="mapa_ruta.html")->None:

	coordenadas_agregadas=[]

	mapa=folium.Map(location=INICIO_MAPA, zoom_start=11)

	for numero_tramo, tramo in tramos.items():

		tipo, linea, origen, destino=tramo["tipo"], tramo["linea"], tramo["origen"], tramo["destino"]

		descripcion_origen=origen["descripcion"] if tipo!="Bus" else f"INICIO BUS - Linea {linea}"

		descripcion_destino=destino["descripcion"] if tipo!="Bus" else f"FIN BUS - Linea {linea}"

		agregarPuntoMarker(origen["punto"].y, origen["punto"].x, origen["nombre"], descripcion_origen, tipo, coordenadas_agregadas, mapa)

		agregarPuntoMarker(destino["punto"].y, destino["punto"].x, destino["nombre"], descripcion_destino, tipo, coordenadas_agregadas, mapa)

		if tipo=="Bus":

			for parada_ruta in tramo["ruta"][1:-1]:

				agregarPuntoMarker(parada_ruta["punto"].y, parada_ruta["punto"].x, "", parada_ruta["descripcion"], tipo, coordenadas_agregadas, mapa, True)

			agregarLinea(tramo["itinerario"]["linea"], mapa)

	ruta_templates=os.path.join(ruta, "templates", "templates_mapas_ruta")

	ruta_archivo_html=os.path.join(ruta_templates, nombre_html)

	mapa.save(ruta_archivo_html)