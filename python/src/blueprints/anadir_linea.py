from flask import Blueprint, render_template, request, redirect

from src.database.conexion import Conexion

bp_anadir_linea=Blueprint("anadir_linea", __name__)

@bp_anadir_linea.route("/anadir_linea")
def anadirLinea():

	con=Conexion()

	lineas_no_recorridas=con.obtenerLineasRecorridas(False)

	con.cerrarConexion()

	return render_template("anadir_linea.html", lineas=lineas_no_recorridas)

@bp_anadir_linea.route("/insertar_linea", methods=["POST"])
def insertarLinea():

	id_linea=request.form.get("linea")

	con=Conexion()

	if not con.existe_linea(id_linea):

		return redirect("/")

	con.anadirLineaRecorrida(id_linea)

	con.cerrarConexion()

	return redirect("/")