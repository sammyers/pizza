from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired
from models import Topping

toppings = [(topping.name, topping.name.title()) for topping in Topping.query.all()]
toppings.insert(0, ('None', 'None'))
locations = [('WH', 'West Hall'), ('EH', 'East Hall'), ('AC', 'Academic Center')]

class OrderForm(Form):
	email = StringField('Email', validators=[InputRequired()])
	item = RadioField('Item', choices=[('half', 'Large half pizza'), ('whole', 'Large whole pizza'), ('other', 'Other')], default='half')
	otherfield = StringField('Other')
	topping1 = SelectField('Topping 1', choices=toppings, default='None')
	topping2 = SelectField('Topping 2', choices=toppings, default='None')
	topping3 = SelectField('Topping 3', choices=toppings, default='None')
	location = SelectField('Location', choices=locations)