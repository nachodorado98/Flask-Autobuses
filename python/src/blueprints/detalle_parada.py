from flask import Blueprint, render_template, redirect

from src.database.conexion import Conexion

bp_detalle_parada=Blueprint("detalle_parada", __name__)

@bp_detalle_parada.route("/detalle_parada/<parada>")
def detalle_parada(parada:int):

	con=Conexion()

	if not con.existe_parada(parada):

		return redirect("/")

	if not con.es_favorita(parada):

		return redirect("/")	

	parada, nombre, comentario, zona, lat, lon, ciudad, barrio, distrito, lineas=con.detalle_parada(parada)

	con.cerrarConexion()

	return render_template("detalle_parada.html",
							parada=parada,
							nombre=nombre,
							comentario=comentario,
							zona=zona,
							latitud=lat,
							longitud=lon,
							ciudad=ciudad,
							barrio=barrio,
							distrito=distrito,
							lineas=lineas)