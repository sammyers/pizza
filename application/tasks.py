from factory import create_celery
from celery.signals import task_prerun
from flask import g
from models import Config, Half, Pizza
from __init__ import app, db
from helpers import add_pizzas

celery = create_celery(app)

@task_prerun.connect
def celery_prerun(*args, **kwargs):

	with celery.app.app_context():

		print db
		print g

@celery.task(ignore_result=True)
def close_order():
	config = db.session.query(Config).first()
	config.state = 'ordered'
	config.timer_id = None
	db.session.commit()
	add_pizzas()
