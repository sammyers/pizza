from flask.ext.wtf import Form
from flask.ext.wtf.html5 import NumberInput
from wtforms import StringField, BooleanField, RadioField, SelectField, SubmitField
from wtforms.validators import InputRequired
from models import Topping
from constants import CAMPUS_LOCATIONS, ORDER_TIMES

toppings = [(topping.name, topping.name.title()) for topping in Topping.query.all()]
toppings.insert(0, ('None', 'None'))
locations = CAMPUS_LOCATIONS
sauces = [('Tomato', 'Robust Inspired'), ('Marinara', 'Hearty Marinara'), ('BBQ', 'BBQ'), ('White', 'Garlic Parmesan'), ('Alfredo', 'Alfredo')]

class OrderForm(Form):
	email = StringField('Email', validators=[InputRequired()])
	item = RadioField('Item', choices=[('half', 'Large half pizza'), ('whole', 'Large whole pizza'), ('medium', 'Medium pizza')], default='half')
	otherfield = StringField('Other')
	topping1 = SelectField('Topping 1', choices=toppings, default='None')
	topping2 = SelectField('Topping 2', choices=toppings, default='None')
	topping3 = SelectField('Topping 3', choices=toppings, default='None')
	topping4 = SelectField('Topping 4', choices=toppings, default='None')
	topping5 = SelectField('Topping 5', choices=toppings, default='None')
	topping6 = SelectField('Topping 6', choices=toppings, default='None')
	location = SelectField('Location', choices=locations)
	sauce = SelectField('Sauce', choices=sauces, default='Tomato')
	price = StringField('Price')

class AdminPanel(Form):
	start = SubmitField('Start Order')
	close = SubmitField('Close Order')
	cancel = SubmitField('Cancel Order')
	settime = SubmitField('Set')
	arrived = SubmitField('Confirm Arrival')
	addtime = SubmitField('Add Time')
	updatetime = SubmitField('Update Time')
	deadline = StringField('Order Period', widget=NumberInput(), default="30")
	deadline_add = StringField('Add to Order Period', widget=NumberInput(), default="5")
	arrivalmin = StringField('Minimum Time', widget=NumberInput(), default='25')
	arrivalmax = StringField('Maximum Time', widget=NumberInput(), default='35')

times = ORDER_TIMES

class RequestForm(Form):
	request_email = StringField('Email', validators=[InputRequired()])
	time = SelectField('Time', choices=times)
