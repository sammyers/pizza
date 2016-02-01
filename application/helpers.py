import datetime
from __init__ import db
from models import Half, Pizza, Person, Topping
from constants import LARGE_PRICE, MEDIUM_PRICE
from algorithm import pizzalgorithm

class ReadablePizza(object):
	def __init__(self, pizza):
		if not hasattr(pizza, 'size'):
			self.size = 'Half'
			self.toppings = [pizza.topping1, pizza.topping2, pizza.topping3]
			self.toppings = filter(None, self.toppings)
			self.list_toppings = ', '.join(self.toppings).title()
			self.email = pizza.email.split('@')[0]
			self.location = pizza.location
		else:
			self.size = pizza.size
			self.toppings = {"Left": [pizza.topping1_left, pizza.topping2_left, pizza.topping3_left],
							 "Right": [pizza.topping1_right, pizza.topping2_right, pizza.topping3_right]}
			self.toppings['Left'] = filter(None, self.toppings['Left'])
			self.toppings['Right'] = filter(None, self.toppings['Right'])
			self.list_toppings = 'Left: {}; Right: {}'.format(
				', '.join(self.toppings['Left']).title(),
				', '.join(self.toppings['Right']).title())
			self.email = pizza.person1.email.split('@')[0]
			self.location = pizza.person1.location
		self.time = datetime.datetime.strftime(pizza.time_added, '%I:%M %p').lstrip('0')

def set_price(form):
	if hasattr(form, 'sauce'):
		sauce = form.sauce.data
	else:
		sauce = 'Tomato'
	location = form.location.data
	size = form.item.data

	if location == 'WH' or location == 'Anywhere':
		delivery = 0
	elif location == 'EH':
		delivery = 0.5
	else:
		delivery = 1

	if sauce == 'Tomato':
		specialsauce = 0
	else:
		specialsauce = 2

	if size == 'half':
		baseprice = LARGE_PRICE / 2
	elif size == 'whole':
		baseprice = LARGE_PRICE
	else:
		baseprice = MEDIUM_PRICE

	total = baseprice + delivery + specialsauce
	return total

def get_pairs(halves):
	toppings = {topping.name:topping.id for topping in db.session.query(Topping).all()}
	toppings['None'] = 0
	halves_by_id = {}
	for half in halves:
		halves_by_id[half.id] = (toppings[half.topping1], toppings[half.topping2], toppings[half.topping3])
	return pizzalgorithm(halves_by_id)

def make_whole_pizzas(halves):
	pairs = get_pairs(halves)
	wholes = []
	for pair in pairs:
		if len(pair) == 2:
			half1 = db.session.query(Half).filter_by(id=pair[0]).first()
			half2 = db.session.query(Half).filter_by(id=pair[1]).first()
			person1 = Person(email=half1.email, location=half1.location)
			person2 = Person(email=half2.email, location=half2.location)
			whole = Pizza(person1=person1, person2=person2)
			whole.topping1_left = half1.topping1
			whole.topping2_left = half1.topping2
			whole.topping3_left = half1.topping3
			whole.topping1_right = half2.topping1
			whole.topping2_right = half2.topping2
			whole.topping3_right = half2.topping3
			whole.sauce = 'Tomato'
			whole.size = 'Large'
			whole.time_added = datetime.datetime.now()
			wholes.append(whole)
	return wholes
