from flask import Blueprint, render_template, redirect, send_file
import os

from src.database.conexion import Conexion

from src.utilidades.utils import eliminarPosiblesMapasFolium, crearMapaFoliumRecorrido

bp_recorrido_linea=Blueprint("recorrido_linea", __name__)

@bp_recorrido_linea.route("/recorrido_linea/<id_linea>")
def recorrido_linea(id_linea:int):

	con=Conexion()

	if not con.existe_linea(id_linea):

		return redirect("/")

	paradas_ida, paradas_vuelta=con.obtenerRecorridoLinea(id_linea)

	barrios=con.barrios_linea(id_linea)

	linea=con.nombre_linea(id_linea)

	con.cerrarConexion()

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	nombre_mapa=f"mapa_recorrido_linea_{id_linea}.html"

	eliminarPosiblesMapasFolium(ruta, "templates_mapas_recorrido", "mapa_recorrido_linea")

	crearMapaFoliumRecorrido(ruta, barrios, paradas_ida, paradas_vuelta, nombre_mapa)

	return render_template("recorrido_linea.html",
							id_linea=id_linea,
							linea=linea,
							nombre_mapa=nombre_mapa)

@bp_recorrido_linea.route("/visualizar_mapa_recorrido/<nombre_mapa>")
def visualizarMapaRecorrido(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "templates_mapas_recorrido", nombre_mapa)

	return send_file(ruta_mapa)