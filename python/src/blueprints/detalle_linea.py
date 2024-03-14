from flask import Blueprint, render_template, redirect

from src.database.conexion import Conexion

bp_detalle_linea=Blueprint("detalle_linea", __name__)

@bp_detalle_linea.route("/detalle_linea/<id_linea>")
def detalle_linea(id_linea:int):

	con=Conexion()

	if not con.existe_linea(id_linea):

		return redirect("/")

	linea, inicio, fin, tipo=con.obtenerDetalleLinea(id_linea)

	total_paradas=con.numero_paradas(id_linea)

	paradas_ida=con.numero_paradas_sentido(id_linea, "IDA")

	paradas_vuelta=con.numero_paradas_sentido(id_linea, "VUELTA")

	con.cerrarConexion()

	return render_template("detalle_linea.html",
							linea=linea,
							inicio_linea=inicio,
							fin_linea=fin,
							tipo_linea=tipo,
							total_paradas=total_paradas,
							paradas_ida=paradas_ida,
							paradas_vuelta=paradas_vuelta)