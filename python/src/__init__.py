from flask import Flask

from .blueprints.blueprint import bp

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	app=Flask(__name__)

	app.config.from_object(configuracion)

	app.register_blueprint(bp)

	return app