from flask import Blueprint, render_template, redirect

from src.database.conexion import Conexion

bp_paradas_favoritas=Blueprint("paradas_favoritas", __name__)

@bp_paradas_favoritas.route("/paradas_favoritas")
def paradas_favoritas():

	con=Conexion()

	paradas=con.paradas_favoritas()

	con.cerrarConexion()

	return render_template("paradas_favoritas.html", paradas=paradas)

@bp_paradas_favoritas.route("/eliminar_parada_favorita/<parada>")
def eliminarParadasFavoritas(parada:int):

	con=Conexion()

	con.eliminarParadaFavorita(parada)

	con.cerrarConexion()

	return redirect("/paradas_favoritas")