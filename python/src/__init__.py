from flask import Flask

from .blueprints.inicio import bp_inicio
from .blueprints.anadir_linea import bp_anadir_linea
from .blueprints.detalle_linea import bp_detalle_linea
from .blueprints.anadir_parada import bp_anadir_parada
from .blueprints.paradas_favoritas import bp_paradas_favoritas

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_anadir_linea)
	app.register_blueprint(bp_detalle_linea)
	app.register_blueprint(bp_anadir_parada)
	app.register_blueprint(bp_paradas_favoritas)

	return app