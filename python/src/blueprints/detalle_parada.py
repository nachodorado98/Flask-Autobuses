from flask import Blueprint, render_template, redirect, send_file
import os

from src.database.conexion import Conexion

from src.utilidades.utils import eliminarPosiblesMapasFolium, crearMapaFolium

bp_detalle_parada=Blueprint("detalle_parada", __name__)

@bp_detalle_parada.route("/detalle_parada/<parada>")
def detalle_parada(parada:int):

	con=Conexion()

	if not con.existe_parada(parada):

		return redirect("/")

	if not con.es_favorita(parada):

		return redirect("/")	

	numero_parada, nombre, comentario, zona, lat, lon, ciudad, barrio, distrito, lineas=con.detalle_parada(parada)

	con.cerrarConexion()

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	nombre_mapa=f"mapa_parada_{parada}.html"

	eliminarPosiblesMapasFolium(ruta)

	datos_parada={"parada":nombre, "numero_parada":numero_parada, "latitud":lat, "longitud":lon}

	crearMapaFolium(ruta, [barrio], datos_parada, nombre_mapa)

	return render_template("detalle_parada.html",
							parada=numero_parada,
							nombre=nombre,
							comentario=comentario,
							zona=zona,
							ciudad=ciudad,
							barrio=barrio,
							distrito=distrito,
							lineas=lineas,
							nombre_mapa=nombre_mapa)

@bp_detalle_parada.route("/visualizar_mapa_parada/<nombre_mapa>")
def visualizarMapaParada(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "templates_mapas_paradas", nombre_mapa)

	return send_file(ruta_mapa)