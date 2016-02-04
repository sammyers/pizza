from algorithm import ToppingCombo

class FoodOrder(object):
	def __init__(self, email, foodtype, location):
		self.email = email
		self.foodtype = foodtype
		self.location = location

class PizzaHalf(FoodOrder):
	def __init__(self, email, location, toppings, veg):
		super(PizzaHalf, self).__init__(email=email, location=location, foodtype='Half Pizza')
		self.toppings = toppings
		self.veg = veg

class PizzaWhole(FoodOrder):
	def __init__(self, email, location, left_toppings, right_toppings, sauce):
		super(PizzaWhole, self).__init__(email=email, location=location, foodtype='Whole Pizza')
		self.toppings = ToppingCombo(left_toppings, right_toppings)
		self.sauce = sauce

class PizzaOrder(object):
	def __init__(self, *args):
		if len(args) == 2 and args[0].foodtype == args[1].foodtype == 'Half Pizza':
			print "Halves"
		elif len(args) == 1 and args[0].foodtype == 'Whole Pizza':
			print "Whole"
		else:
			raise TypeError('Incompatible orders!')