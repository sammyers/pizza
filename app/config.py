import os
from constants import DATABASE_URI, SECRET_KEY

class Config:

	@staticmethod
	def init_app(app):
		pass

class LocalConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = DATABASE_URI
	CELERY_BROKER_URL = 'amqp://guest@localhost//'
	SECRET_KEY = SECRET_KEY
	SQLALCHEMY_ECHO = True
	CELERY_IMPORTS = ('application.tasks')

config = {
	'local': LocalConfig
}

SELECTED_CONFIG = 'local'
