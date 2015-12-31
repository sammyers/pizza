from flask import Flask, flash, redirect, render_template, request, session
import requests
from application import app, db
from application.forms import OrderForm
from application.models import Config, Half
from application.constants import CONSUMER_ID, CONSUMER_SECRET, APP_SECRET

app.debug = True
app.secret_key = APP_SECRET

@app.route("/") 
def homepage():
	homepage_state = Config.query.filter_by(setting='homepage state').first().value

	if homepage_state == 'ordering':
		food = Config.query.filter_by(setting='food').first().value
		time = Config.query.filter_by(setting='order time').first().value
		return render_template('homepage_ordering.html', food=food, time=time)
	elif homepage_state == 'ordered':
		arriving = Config.query.filter_by(setting='arrival time').first().value
		return render_template('homepage_ordered.html', arriving=arriving)
	else:
		return render_template('homepage.html')

@app.route("/order", methods=['GET', 'POST'])
def order():
	time = Config.query.filter_by(setting='order time').first().value
	food = Config.query.filter_by(setting='food').first().value
	form = OrderForm(request.form)
	if request.method == 'POST' and form.validate():
		order = Half()
		order.email = form.email.data + '@students.olin.edu'
		order.location = form.location.data
		order.topping1 = form.topping1.data
		order.topping2 = form.topping2.data
		order.topping3 = form.topping3.data
		db.session.add(order)
		db.session.commit()
		return redirect('/pay')
	return render_template('order.html', time=time, food=food, form=form)

@app.route("/pay", methods=['GET','POST'])
def pay():
	# form = PaymentForm(request.form)
	return render_template('payment.html')

@app.route("/request", methods=['GET','POST'])
def request_food():
	return render_template('request.html')

@app.route("/done")
def done():
	return render_template('done.html')

@app.route("/admin")
def admin():
	return render_template('admin.html')

if __name__ == "__main__":
	app.run()