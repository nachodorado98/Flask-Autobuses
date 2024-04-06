from flask import Blueprint, render_template, request, jsonify, redirect, current_app, send_file
import os

from src.database.conexion import Conexion

from src.utilidades.utils import hora_actual, paradas_validas, hora_valida, obtenerDatosParada
from src.utilidades.utils import obtenerHoraMinutos, obtenerDatosRecorrido, eliminarPosiblesMapasFolium
from src.utilidades.utils import crearMapaFoliumRuta, obtenerPasosDetalleRuta

bp_llevame=Blueprint("llevame", __name__)

@bp_llevame.route("/llevame")
def llevame():

	con=Conexion()

	paradas_origen=con.obtener_paradas()

	con.cerrarConexion()

	return render_template("llevame.html",
							paradas_origen=paradas_origen,
							hora=hora_actual())

@bp_llevame.route("/posibles_paradas_destino")
def posibles_paradas_destino():

	parada_origen=request.args.get("parada_origen")

	con=Conexion()

	paradas_destino=con.obtener_paradas(parada_origen)

	con.cerrarConexion()

	return jsonify(paradas_destino)

@bp_llevame.route("/llevame/ruta", methods=["POST"])
def obtenerRuta():

	origen=request.form.get("parada-origen")
	destino=request.form.get("parada-destino")
	hora=request.form.get("hora")

	if not paradas_validas(origen, destino) or not hora_valida(hora):

		return redirect("/llevame")

	con=Conexion()

	if not con.existe_parada(int(origen)) or not con.existe_parada(int(destino)):

		con.cerrarConexion()

		return redirect("/llevame")

	con.cerrarConexion()

	correo, contrasena=current_app.config.get("CORREO"), current_app.config.get("CONTRASENA")

	datos_parada_origen=obtenerDatosParada(correo, contrasena, origen)

	datos_parada_destino=obtenerDatosParada(correo, contrasena, destino)

	if not datos_parada_origen or not datos_parada_destino:

		return redirect("/llevame")

	horas, minutos=obtenerHoraMinutos(hora)

	datos_recorrido=obtenerDatosRecorrido(correo,
											contrasena,
											datos_parada_origen["latitud"],
											datos_parada_origen["longitud"],
											datos_parada_origen["direccion"],
											datos_parada_destino["latitud"],
											datos_parada_destino["longitud"],
											datos_parada_destino["direccion"],
											horas,
											minutos)

	if not datos_recorrido:

		return redirect("/llevame")

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	nombre_mapa=f"mapa_ruta_{origen}_{destino}.html"

	eliminarPosiblesMapasFolium(ruta, "templates_mapas_ruta", "mapa_ruta")

	crearMapaFoliumRuta(ruta, datos_recorrido["detalle"], nombre_mapa)

	pasos_detalle=obtenerPasosDetalleRuta(datos_recorrido["detalle"])

	return render_template("ruta.html",
							origen=datos_parada_origen["direccion"],
							destino=datos_parada_destino["direccion"],
							salida=datos_recorrido["basico"]["salida"].strftime("%H:%M"),
							llegada=datos_recorrido["basico"]["llegada"].strftime("%H:%M"),
							distancia=datos_recorrido["basico"]["distancia"],
							duracion=datos_recorrido["basico"]["duracion"],
							nombre_mapa=nombre_mapa,
							pasos_detalle=pasos_detalle)

@bp_llevame.route("/visualizar_mapa_ruta/<nombre_mapa>")
def visualizarMapaRuta(nombre_mapa:str):

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_mapa=os.path.join(ruta, "templates", "templates_mapas_ruta", nombre_mapa)

	return send_file(ruta_mapa)