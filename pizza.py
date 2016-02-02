from application import app, db
from flask import redirect, render_template, request, session, jsonify
import requests, datetime, threading, decimal, math
from application.models import Config, Half, Pizza, Person, Request
from application.forms import OrderForm, AdminPanel, RequestForm
from application.constants import CONSUMER_ID, CONSUMER_SECRET 
from application.constants import VENMO_ADMIN, VENMO_NOTE
from application.constants import LARGE_PRICE, MEDIUM_PRICE
from application.constants import EMAIL_DOMAIN, ORDER_TIMES
from application.tasks import close_order
from application.helpers import ReadablePizza, set_price, add_pizzas, clear_tables
from celery.task.control import revoke
from sqlalchemy.exc import IntegrityError


@app.route("/")
def homepage():
	data = db.session.query(Config).first()
	return render_template('homepage.html', data=data)


@app.route("/order", methods=['GET', 'POST'])
def order():
	data = db.session.query(Config).first()
	if data.state != 'ordering':
		return redirect("/")
	form = OrderForm(request.form)
	if request.method == 'POST' and form.validate():
		db.session.expunge_all()
		if form.item.data == 'half':
			order = Half()
			order.email = form.email.data + EMAIL_DOMAIN
			order.location = form.location.data
			order.topping1 = form.topping1.data
			order.topping2 = form.topping2.data
			order.topping3 = form.topping3.data
		elif form.item.data == 'whole':
			order = Pizza()
			person = Person()
			order.topping1_left = form.topping1.data
			order.topping2_left = form.topping2.data
			order.topping3_left = form.topping3.data
			order.topping1_right = form.topping4.data
			order.topping2_right = form.topping5.data
			order.topping3_right = form.topping6.data
			order.sauce = form.sauce.data
			order.size = 'Large'
			person.email = form.email.data + EMAIL_DOMAIN
			person.location = form.location.data
			order.person1 = person
			db.session.add(person)
		elif form.item.data == 'medium':
			order = Pizza()
			person = Person()
			order.topping1_left = form.topping1.data
			order.topping2_left = form.topping2.data
			order.topping1_right = form.topping4.data
			order.topping2_right = form.topping5.data
			order.sauce = form.sauce.data
			order.size = 'Medium'
			person.email = form.email.data + EMAIL_DOMAIN
			person.location = form.location.data
			order.person1 = person
			db.session.add(person)
		order.time_added = datetime.datetime.now()
		db.session.add(order)
		db.session.commit()
		session['payment_amount'] = set_price(form)
		url = 'https://api.venmo.com/v1/oauth/authorize?client_id={}&scope=make_payments&response_type=code'.format(CONSUMER_ID)
		return redirect(url)
	return render_template('order.html', data=data, form=form, domain=EMAIL_DOMAIN, 
						   large_price=LARGE_PRICE, medium_price=MEDIUM_PRICE)


@app.route("/request", methods=['GET','POST'])
def request_food():
	form = RequestForm(request.form)
	times = [time[0] for time in ORDER_TIMES]
	requests = [len(db.session.query(Request).filter_by(time=time).all()) for time in times]
	current = []
	for a, b in zip(times, requests):
		current.append({"time": a, "requests": b})
	if request.method == 'POST' and form.validate():
		db.session.expunge_all()
		try:
			food_request = Request(email=form.request_email.data + EMAIL_DOMAIN, time=form.time.data)
			db.session.add(food_request)
			db.session.commit()
			return redirect("/")
		except IntegrityError:
			db.session.expunge_all()
			return redirect("/request")
	return render_template('request.html', form=form, domain=EMAIL_DOMAIN, current=current)


@app.route("/done")
def done():
	return render_template('done.html')


@app.route("/oauth-authorized")
def oauth_authorized():
	if request.args.get('error'):
		return redirect("/order")
	AUTHORIZATION_CODE = request.args.get('code')
	data = {
		"client_id":CONSUMER_ID,
		"client_secret":CONSUMER_SECRET,
		"code":AUTHORIZATION_CODE,
	}
	url = 'https://api.venmo.com/v1/oauth/access_token'
	response = requests.post(url, data)
	response_dict = response.json()
	access_token = response_dict.get('access_token')
	user = response_dict.get('user')

	session['venmo_token'] = access_token
	session['venmo_username'] = user['username']

	return redirect("/pay")


@app.route("/pay")
def pay():
	if session.get('venmo_token'):
		config = db.session.query(Config).first()
		remaining = config.deadline - datetime.datetime.now()
		data = {
			"username":session['venmo_username'],
			"access_token":session['venmo_token'],
			"amount":session['payment_amount'],
			"eta":"{} to {} minutes".format(
				(remaining.seconds / 60 + config.arrivalmin),
				(remaining.seconds / 60 + config.arrivalmax)
				)
		}
		return render_template('pay.html', data=data)
	else:
		return redirect("/")


@app.route("/make_payment", methods=['POST'])
def make_payment():
	access_token = session['venmo_token']
	note = VENMO_NOTE
	username = VENMO_ADMIN
	amount = session['payment_amount']

	payload = {
		"access_token":access_token,
		"username":username,
		"note":note,
		"amount":amount
	}

	url = "https://api.venmo.com/v1/payments"
	response = requests.post(url, payload)
	data = response.json()
	session.clear()
	db.session.commit()
	return jsonify(data)


@app.route("/check_status", methods=['GET', 'POST'])
def check_status():
	config = db.session.query(Config).first()
	# if request.method == 'POST':
		
	data = {
		"state":config.state,
		"deadline":config.deadline,
		"arrivalmin":config.arrivalmin,
		"arrivalmax":config.arrivalmax
	}
	return jsonify(data)


@app.route("/admin", methods=['GET','POST'])
def admin():
	data = db.session.query(Config).first()
	panel = AdminPanel(request.form)

	if request.method == 'POST':
		db.session.expunge_all()
		config = db.session.query(Config).first()
		if panel.start.data and config.state == 'not ordering':
			clear_tables()
			config.state = 'ordering'
			duration = datetime.timedelta(minutes=int(panel.deadline.data))
			config.deadline = datetime.datetime.now() + duration
			config.arrivalmin = 25
			config.arrivalmax = 35
			timer = close_order.apply_async(countdown=duration.seconds)
			config.timer_id = timer.task_id

		elif panel.close.data and config.state == 'ordering' and int(panel.arrivalmin.data) < int(panel.arrivalmax.data):
			config.state = 'ordered'
			config.deadline = datetime.datetime.now()
			config.arrivalmin = panel.arrivalmin.data
			config.arrivalmax = panel.arrivalmax.data
			revoke(config.timer_id)
			config.timer_id = None
			add_pizzas()

		elif panel.arrived.data and config.state == 'ordered':
			config.state = 'not ordering'
			config.arrivalmin = 0
			config.arrivalmax = 0

		elif panel.cancel.data and config.state == 'ordering':
			config.state = 'not ordering'
			config.deadline = datetime.datetime.now()
			config.arrivalmin = 0
			config.arrivalmax = 0
			revoke(config.timer_id)
			config.timer_id = None

		elif panel.addtime.data and config.state == 'ordering':
			config.deadline = config.deadline + datetime.timedelta(minutes=int(panel.deadline_add.data))
			duration = config.deadline - datetime.datetime.now()
			revoke(config.timer_id)
			timer = close_order.apply_async(countdown=duration.seconds)
			config.timer_id = timer.task_id

		elif panel.settime.data and config.state == 'ordering':
			config.arrivalmin = panel.arrivalmin.data
			config.arrivalmax = panel.arrivalmax.data

		elif panel.updatetime.data and config.state == 'ordered' and int(panel.arrivalmin.data) < int(panel.arrivalmax.data):
			finalmin = config.deadline + datetime.timedelta(minutes=config.arrivalmin)
			finalmax = config.deadline + datetime.timedelta(minutes=config.arrivalmax)
			minleft = math.ceil(float((finalmin - datetime.datetime.now()).seconds) / 60)
			maxleft = math.ceil(float((finalmax - datetime.datetime.now()).seconds) / 60)
			addmin = int(panel.arrivalmin.data) - minleft
			addmax = int(panel.arrivalmax.data) - maxleft
			config.arrivalmin += addmin
			config.arrivalmax += addmax
		db.session.commit()
		return redirect("/admin")

	if data.state == 'ordering':
		half_orders = db.session.query(Half).all()
		whole_orders = db.session.query(Pizza).all()
		orders = [ReadablePizza(pizza) for pizza in half_orders] + [ReadablePizza(pizza) for pizza in whole_orders]
		orders.sort(key=lambda x: x.time)
		return render_template('admin.html', panel=panel, data=data, orders=orders)

	return render_template('admin.html', panel=panel, data=data)


if __name__ == "__main__":
	app.run()
