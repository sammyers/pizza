# from database import db
from celery import Celery
from flask import Flask
from flask import g
from config import config, SELECTED_CONFIG

def create_celery(app=None):
	app = app or create_app()
	celery = Celery("app", broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	TaskBase = celery.Task

	class ContextTask(TaskBase):
		abstract = True

		def __call__(self, *args, **kwargs):
			with app.app_context():
				return TaskBase.__call__(self, *args, **kwargs)

	celery.Task = ContextTask
	celery.app = app
	return celery


# def create_before_request(app):
# 	def before_request():
# 		g.db = db
# 	return before_request


def create_app():
	app = Flask("app")
	app.config.from_object(config[SELECTED_CONFIG])

	# app.before_request(create_before_request(app))
	return app
