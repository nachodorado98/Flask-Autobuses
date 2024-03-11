from flask import Blueprint, render_template

from src.database.conexion import Conexion

bp_inicio=Blueprint("inicio", __name__)

@bp_inicio.route("/")
def inicio():

	con=Conexion()

	lineas_recorridas=con.obtenerLineasRecorridas()

	con.cerrarConexion()

	return render_template("inicio.html", lineas=lineas_recorridas)