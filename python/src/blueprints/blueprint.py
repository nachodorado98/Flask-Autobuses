from flask import Blueprint

bp=Blueprint("blueprint", __name__)

@bp.route("/", methods=["GET"])
def inicio():

	return f"<h1>Hola Mundo</h1>"