import csv
from os import path

import frappe
from frappe.utils import get_site_name

from european_banking_integration.reader import Reader
from european_banking_integration.transformer import Kreissparkasse_transformer
from european_banking_integration.utils import (account_paid_to, get_file_path,
                                                get_paid_from, get_party)

def statement_update(doc, event=None):

	file_path  = get_file_path(doc.import_file)

	if not (file_path.endswith('.csv') or file_path.endswith('xlsx')):
		frappe.throw('Requires CSV File')
		return
	paid_from = frappe.get_doc('Bank Account', doc.bank_account).account		
	paid_from_currency = frappe.get_doc('Account', paid_from).account_currency

	submit_after_save = doc.submit_after_import

	with open(file_path, 'r') as f:
		uploaded_file = Reader(f)

		for row in uploaded_file.read():
			data = Kreissparkasse_transformer(row)	

			make_payment_entry(data['amount'], data['reference_date'], data['iban'], data['reference'], doc.company, paid_from, submit_after_save, data['booking_date'], paid_from_currency)


def make_payment_entry(amount, dt, iban, reference, company, paid_from, submit_after_import, reference_date, paid_from_currency):

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

	payment_entry = frappe.new_doc('Payment Entry')
	payment_entry.payment_type = payment_type
	payment_entry.company = company
	payment_entry.posting_date = dt
	
	payment_entry.party_type = party_type
	payment_entry.party = party
	payment_entry.party_name = party_name
	payment_entry.paid_from = paid_from
	payment_entry.custom_remarks = 1

	payment_entry.remarks = reference,
	payment_entry.reference_no = iban,
	payment_entry.reference_date = reference_date

	payment_entry.paid_from_account_currency = paid_from_currency 
	payment_entry.paid_to = paid_to[0].name

	# payment_entry.paid_to_account_currency = 'CHF'
	payment_entry.paid_amount = abs(amount)
	payment_entry.received_amount = abs(amount)

	# Fraape Commit Message
	frappe.db.commit()
	
	# Insert Payment Entry
	payment_entry.insert()

	if (not(party_name == 'Temp Supplier' or party_name == 'Temp Customer')) and submit_after_import:
		payment_entry.submit()


	
	
