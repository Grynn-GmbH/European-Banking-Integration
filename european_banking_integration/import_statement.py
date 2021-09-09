import frappe
import csv
from frappe.utils import get_site_name
from european_banking_integration.utils import get_file_path, get_party, get_paid_from, account_paid_to
from os import path
from european_banking_integration.reader import Reader
from european_banking_integration.transformer import Kreissparkasse_transformer

def statement_update(doc, event=None):

	file_path  = get_file_path(doc.import_file)

	if not (file_path.endswith('.csv') or file_path.endswith('xlsx')):
		frappe.throw('Requires CSV File')
		return
	
	with open(file_path, 'r') as f:
		uploaded_file = Reader(f)

		for row in uploaded_file.read():
			data = Kreissparkasse_transformer(row)	

			make_payment_entry(data['amount'], data['reference_date'], data['iban'], 'hi', doc.company)


def make_payment_entry(amount, dt, iban, reference, company):

	# Payment Type
	if amount < 0:
		payment_type = 'Pay'
	elif amount > 0:
		payment_type = 'Receive'
	else:
		return

	# Company (company)

	# Posting Date (dt)

	# party Type

	[party_type, party, party_name] = get_party(iban)

	if not party_type:
		return

	# Paid From

	paid_from = get_paid_from(company)

	# Currency

	# Paid to

	paid_to = account_paid_to(company)

	# Amount (amount)

	print(amount,
				paid_from, 
				paid_to, 
				party_type, 
				party, 
				party_name, 
				party_type)


	
	
