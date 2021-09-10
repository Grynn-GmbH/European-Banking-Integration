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
	paid_from = frappe.get_doc('Bank Account', doc.bank_account).account		
	with open(file_path, 'r') as f:
		uploaded_file = Reader(f)

		for row in uploaded_file.read():
			data = Kreissparkasse_transformer(row)	

			make_payment_entry(data['amount'], data['reference_date'], data['iban'], 'hi', doc.company, paid_from)


def make_payment_entry(amount, dt, iban, reference, company, paid_from):

	# Payment Type
	if amount < 0:
		payment_type = 'Pay'
	elif amount > 0:
		payment_type = 'Receive'
	else:
		return

	[party_type, party, party_name] = get_party(iban, payment_type)

	if not party_type:
		if payment_type == 'Pay':
			party_type = 'Supplier'
			party_name = 'Temp Supplier'
			party = 'Temp Supplier'
		else:
			party_type = 'Customer'
			party_name = 'Temp Customer'
			party = 'Temp Customer'
		

	paid_to = account_paid_to(company)

	# Amount (amount)

	payment_entry = frappe.new_doc('Payment Entry')
	payment_entry.payment_type = payment_type
	payment_entry.company = company
	# payment_entry.posting_date = dt
	
	payment_entry.party_type = party_type
	payment_entry.party = party
	payment_entry.party_name = party_name
	payment_entry.paid_from = paid_from

	# TODO: Make Reference No
	payment_entry.reference_no = 'xyz',
	payment_entry.reference_date = '2021-09-10'

	# TODO: Make Currency Dynamic
	# payment_entry.paid_from_account_currency = 'CHF'
	payment_entry.paid_to = paid_to[0].name

	# TODO: Make Currency Dynamic
	# payment_entry.paid_to_account_currency = 'CHF'
	payment_entry.paid_amount = abs(amount)
	payment_entry.received_amount = abs(amount)

	# Fraape Commit Message
	frappe.db.commit()
	
	# Insert Payment Entry
	payment_entry.insert()
	
	# payment_entry.submit()


	
	
