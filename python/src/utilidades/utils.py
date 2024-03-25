import os
from typing import List, Dict
import geopandas as gpd
import folium

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