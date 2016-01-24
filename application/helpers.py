import datetime

class ReadablePizza(object):
	def __init__(self, pizza):
		if not hasattr(pizza, 'size'):
			self.size = 'Half'
			self.toppings = [pizza.topping1, pizza.topping2, pizza.topping3]
			self.email = pizza.email.split('@')[0]
			self.location = pizza.location
		else:
			self.size = pizza.size
			self.toppings = {"Left": [pizza.topping1_left, pizza.topping2_left, pizza.topping3_left],
							 "Right": [pizza.topping1_right, pizza.topping2_right, pizza.topping3_right]}
			self.email = pizza.person1.email.split('@')[0]
			self.location = pizza.person1.location
		self.time = datetime.datetime.strftime(pizza.time_added, '%I:%M %p').lstrip('0')
