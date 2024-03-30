from flask import Flask
import os

from .blueprints.inicio import bp_inicio
from .blueprints.anadir_linea import bp_anadir_linea
from .blueprints.detalle_linea import bp_detalle_linea
from .blueprints.anadir_parada import bp_anadir_parada
from .blueprints.paradas_favoritas import bp_paradas_favoritas
from .blueprints.detalle_parada import bp_detalle_parada
from .blueprints.recorrido_linea import bp_recorrido_linea
from .blueprints.llevame import bp_llevame

from .utilidades.utils import crearCarpeta

# Funcion para crear el entorno
def creacionEntorno()->None:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	ruta_src=os.path.join(ruta, "src")

	crearCarpeta(os.path.join(ruta_src, "templates", "templates_mapas_paradas"))
	crearCarpeta(os.path.join(ruta_src, "templates", "templates_mapas_recorrido"))

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_anadir_linea)
	app.register_blueprint(bp_detalle_linea)
	app.register_blueprint(bp_anadir_parada)
	app.register_blueprint(bp_paradas_favoritas)
	app.register_blueprint(bp_detalle_parada)
	app.register_blueprint(bp_recorrido_linea)
	app.register_blueprint(bp_llevame)

	creacionEntorno()

	return app