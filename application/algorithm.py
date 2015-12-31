from sets import Set

def ToppingCombo(left_toppings, right_toppings):
	left = Set(left_toppings)
	right = Set(right_toppings)
	both = left | right
	toppings = {'whole':[], 'left':[], 'right':[]}
	for item in both:
		if item in left & right:
			toppings['whole'].append(item)
		elif item in left:
			toppings['left'].append(item)
		else:
			toppings['right'].append(item)
	return toppings

def Optimize(*args):

	return pizzas