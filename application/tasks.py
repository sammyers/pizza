from factory import create_celery
from celery.signals import task_prerun
from flask import g
from models import Config, Half, Pizza
from __init__ import app, db
from helpers import add_pizzas
import datetime

celery = create_celery(app)

@task_prerun.connect
def celery_prerun(*args, **kwargs):

	with celery.app.app_context():

		print db
		print g

@celery.task(ignore_result=True)
def close_order():
	add_pizzas()
	large_coupon = len(db.session.query(Pizza).filter_by(size='Large').all())
	medium_coupon = len(db.session.query(Pizza).filter_by(size='Medium').all())
	if db.session.query(Half).all() != [] or 0 < large_coupon < 2 or 0 < medium_coupon < 2:
		config = db.session.query(Config).first()
		config.deadline = datetime.datetime.now() + datetime.timedelta(minutes=5)
		timer = close_order.apply_async(countdown=300)
		config.timer_id = timer.task_id
		db.session.commit()
	else:
		config = db.session.query(Config).first()
		config.state = 'ordered'
		config.timer_id = None
		db.session.commit()
