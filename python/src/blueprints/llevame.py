from flask import Blueprint, render_template, request, jsonify

from src.database.conexion import Conexion

from src.utilidades.utils import hora_actual

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