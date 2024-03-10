class Config():

	SECRET_KEY="password"

class DevelopmentConfig(Config):

	DEBUG=True

config={"development":DevelopmentConfig()}