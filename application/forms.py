from flask.ext.wtf import Form
from flask.ext.wtf.html5 import NumberInput
from wtforms import StringField, BooleanField, RadioField, SelectField, SubmitField
from wtforms.validators import InputRequired
from models import Topping

toppings = [(topping.name, topping.name.title()) for topping in Topping.query.all()]
toppings.insert(0, ('None', 'None'))
locations = [('WH', 'West Hall'), ('EH', 'East Hall'), ('AC', 'Academic Center')]

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
	left_toppings = [SelectField('Topping {}'.format(number), choices=toppings, default='None') for number in range(1,4)]
	right_toppings = [SelectField('Topping {}'.format(number), choices=toppings, default='None') for number in range(1,4)]

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
