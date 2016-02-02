"""
Credit: Matthew Beaudouin

 Mixing half pizzas together such that we maximize the overlap of toppings.
 In this version, we consider 3 toppings (pizza is an object)
 This algorithm looks for matches of 3s, then 2s, then 1s 
"""

import random

# numTops = 1+10# Thanks MySQL

# #Generate a random list of half pizzas
# orderSize = 11
# randomOrders = {1: {random.randint(1, numTops),random.randint(1, numTops),random.randint(1, numTops)}}	# Make first order
# for i in range(2, orderSize+1):
# 	randomOrders[i] = {random.randint(1, numTops),random.randint(1, numTops),random.randint(1, numTops)} # Add orders

# knownOrder = {1: (1,2,3), 2:(8,4,6), 3:(0,2,5), 4:(4,6), 5:(1,2,3), 6:(10,11,12)}  

# edgeCase = {1: (1,2,3), 2:(1,2,3), 3:(1,2,3), 4:(1,2,3), 5:(1,2,3)}


def pizzalgorithm(gimmeDemHalves):
	""" 
	Takes a dictionary of key-tuple, where the key is the pizza ID and the tuple contains the topping IDs. 
	Returns a list of tuples, where each tuple contains two half pizza IDs (to be put together). 
	If there is an odd number of half pizzas given, the last element will be a 1-tuple.
	"""

	printbool = False # Make true for debugging

	
	pizzaHalves = dict() # Convert key-tuple dictionary to key-set dictionary 'cause I'm a cookster.
	remainingPizzas = [] # IDs of Pizzas that have not yet been paired. The list will make it easier to tell which is which

	for key in gimmeDemHalves:
		pizzaHalves[key] = set(gimmeDemHalves[key])
		remainingPizzas.append(key)

	# The list to be returned. It will contain tuples of the relavent half pizzas
	CombinedPizzas = [] 

	# Remove all perfect (3) combinations, then 2 combinations, then 1 combinations
	n = 3

	while len(remainingPizzas) < 0 or n!=-1:
		nfound = False
		choice1 = 0
		choice2 = 1

		if printbool:
			print 'n:', n
			print 'Number of remaining pizzas:', len(remainingPizzas)

		while choice1 < len(remainingPizzas) and  not (nfound):
			while choice2 < len(remainingPizzas) and not (nfound):
				if printbool: print choice1, choice2, pizzaHalves[remainingPizzas[choice1]], pizzaHalves[remainingPizzas[choice2]]
				if (choice1 != choice2 and len(pizzaHalves[remainingPizzas[choice1]] & pizzaHalves[remainingPizzas[choice2]]) == n):
					nfound = True
					chosenOne = choice1 # Keep track of them because of post-increments tomfoolery
					chosenTwo = choice2 

				choice2 += 1
			choice1 += 1
			choice2 = choice1+1 	

		if nfound: # A pair is found (and the loop was interrupted)
			#print "Found something"
			choice1 -= 1 	# Take into account that when leaving the double loop, both are exceedingly incremented
			choice2 -= 1

			# Add the glorious pizzas
			CombinedPizzas.append( (remainingPizzas[chosenOne], remainingPizzas[chosenTwo]) )
			if printbool: print "These Pizzas:", pizzaHalves[remainingPizzas[chosenOne]], '+', pizzaHalves[remainingPizzas[chosenTwo]]

			# Remove from orders
			del remainingPizzas[chosenTwo] # Delete the larger one first such that you don't mess with the other's position in the list
			del remainingPizzas[chosenOne] # Due to how the loop is made, choice1<choice2

		else:	# If the loop went to completion, reduce match you are looking for
			n -= 1

	if len(remainingPizzas):
		CombinedPizzas.append( (remainingPizzas[0],) )

	return CombinedPizzas

# whatYouWant = pizzalgorithm(edgeCase)

# print randomOrders
# print "Pairs: "
# for i in range(0, len(whatYouWant)):
# 	print whatYouWant[i]

# from sets import Set

# def ToppingCombo(left_toppings, right_toppings):
# 	left = Set(left_toppings)
# 	right = Set(right_toppings)
# 	both = left | right
# 	toppings = {'whole':[], 'left':[], 'right':[]}
# 	for item in both:
# 		if item in left & right:
# 			toppings['whole'].append(item)
# 		elif item in left:
# 			toppings['left'].append(item)
# 		else:
# 			toppings['right'].append(item)
# 	return toppings