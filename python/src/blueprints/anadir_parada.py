from flask import Blueprint, render_template, redirect, request

from src.database.conexion import Conexion

bp_anadir_parada=Blueprint("anadir_parada", __name__)

@bp_anadir_parada.route("/anadir_parada/<id_linea>")
def anadirParada(id_linea:int):

	con=Conexion()

	if not con.existe_linea(id_linea):

		return redirect("/")

	linea=con.nombre_linea(id_linea)

	paradas_no_favoritas=con.paradas_no_favoritas(id_linea)

	con.cerrarConexion()

	return render_template("anadir_parada.html",
							linea=linea,
							id_linea=id_linea,
							paradas=paradas_no_favoritas)


@bp_anadir_parada.route("/insertar_parada", methods=["POST"])
def insertarParada():

	parada=request.form.get("parada")

	con=Conexion()

	if not con.existe_parada(parada):

		return redirect("/")

	con.anadirParadaFavorita(parada)

	con.cerrarConexion()

	return redirect("/")