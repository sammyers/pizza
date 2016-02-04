import smtplib
from email.mime.text import MIMEText
from constants import ADMIN_EMAIL, EMAIL_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD, PICKUP_LOCATION
from helpers import topping_combo
from decimal import Decimal
from __init__ import db
from models import Pizza

url = EMAIL_SERVER
user = EMAIL_USERNAME
password = EMAIL_PASSWORD

def pizza_details(order, amount):
	total = 'Total: ${}'.format(str(Decimal(amount).quantize(Decimal('0.01'))))
	if hasattr(order, 'size'):
		size = order.size
		left = [order.topping1_left, order.topping2_left, order.topping3_left]
		right = [order.topping1_right, order.topping2_right, order.topping3_right]
		toppings = topping_combo(left, right)
		toppings['Left'] = ', '.join(filter(lambda x: x != 'None', toppings['Left']))
		toppings['Right'] = ', '.join(filter(lambda x: x != 'None', toppings['Right']))
		toppings['Whole'] = ', '.join(filter(lambda x: x != 'None', toppings['Whole']))
		toppinglist = '\n'.join(sorted(['\t' + key + ': ' + value for (key, value) in toppings.items() if value  != '']))
		if toppinglist != '':
			if order.sauce == 'Tomato':
				details = '{} pizza\n'.format(size) + 'Toppings:\n' + toppinglist + '\n' + total
			else:
				details = '{} pizza with {} sauce\n'.format(size, order.sauce.lower()) + 'Toppings:\n' + toppinglist + '\n' + total
		else:
			if order.sauce == 'Tomato':
				details = '{} cheese pizza\n'.format(size) + '\n' + total
			else:
				details = '{} cheese pizza with {} sauce\n'.format(size, order.sauce.lower()) + '\n' + total
	else:
		size = 'Large half'
		toppings = ', '.join(filter(lambda x: x != 'None', [order.topping1, order.topping2, order.topping3]))
		if toppings != '':
			details = '{} pizza\n'.format(size) + 'Toppings: ' + toppings + '\n' + total
		else:
			details = '{} cheese pizza\n'.format(size) + '\n' + total
	return details

def send_email(body, recipients, order=True):
	message = MIMEText(body)
	
	message['From'] = ADMIN_EMAIL
	message['To'] = ', '.join(recipients)
	if order == True:
		message['Subject'] = 'Consamables Order Confirmation'
	else:
		message['Subject'] = 'Consamables Arrival Confirmation'

	connection = smtplib.SMTP(EMAIL_SERVER, 587)
	connection.ehlo()
	connection.starttls()
	connection.ehlo()
	connection.login(EMAIL_USERNAME, EMAIL_PASSWORD)
	connection.sendmail(ADMIN_EMAIL, recipients, message.as_string())
	connection.close()

def order_confirmation(order, amount):
	body = """Thanks for your order! You'll receive another notification when your food has arrived. You ordered:
	\n{}""".format(pizza_details(order, amount))

	if hasattr(order, 'email'):
		recipients = [order.email]
	else:
		try:
			recipients = [order.person1.email, order.person2.email]
		except AttributeError:
			recipients = [order.person1.email]
	send_email(body, recipients)

def arrival_confirmation():
	orders = db.session.query(Pizza).all()
	body_base = "Your food has arrived! "
	share = "You're sharing a pizza with {}. "
	location = "Unless you requested delivery to another part of campus, come to {}!".format(PICKUP_LOCATION)
	for order in orders: 
		if order.person2 is not None:
			body1 = body_base + share.format(order.person2.email.split('@')[0].replace('.', ' ').title()) + location
			body2 = body_base + share.format(order.person1.email.split('@')[0].replace('.', ' ').title()) + location
			recipient1 = [order.person1.email]
			recipient2 = [order.person2.email]
			send_email(body1, recipient1, order=False)
			send_email(body2, recipient2, order=False)
		else: 
			body = body_base + location
			recipients = [order.person1.email]
			send_email(body, recipients, order=False)