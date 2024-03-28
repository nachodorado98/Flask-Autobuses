class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True

	# Añadir correo y contraseña de la API EMT
	CORREO=""
	CONTRASENA=""

config={"development":DevelopmentConfig()}