# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from european_banking_integration.reader import Reader
from european_banking_integration.utils import find_company, get_party, get_paid_from, account_paid_to

__version__ = '0.0.1'



@frappe.whitelist()
def upload_bank_statement(statement):
		

		iban = 'DE75370800400232113001'

		if not find_company(iban):
			return

		[party_type, customer, customer_name] = get_party(iban)		


		paid_from = get_paid_from(iban)

		paid_from = account_paid_to(iban)

		account_currency = frappe.get_doc('Account', paid_from).currency



