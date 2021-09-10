import frappe
from os import path


def get_file_path(location):
	site_path = frappe.get_site_path()
	return site_path + location

def find_party(iban):
	bank_account = frappe.get_list(
		'Bank Account', filters=[['iban', '=', iban]])
		
	if len(bank_account) > 0:
		party = frappe.get_doc('Bank Account', bank_account[0])
		return [party.party_type, party.party, party.party]
	else:
		return [False, False, False]

def find_company(iban):
	[company] = frappe.get_list('Bank Account', filters=[['iban', '=', iban], ["is_company_account", "=", 1]], fields=['company'])	
	return company


def get_paid_from(company):

	filters = [
		["company", "=", company],
		["is_group", "=", 0],
		["account_type", "=", "Payable"]
	]
	return frappe.db.get_list('Account', filters=filters)
	

def account_paid_to(company):
	filters = [
		["company", "=", company],
		["is_group", "=", 0],
		["account_type", "in", ["Bank", "Cash"]]
	]
	return frappe.db.get_list('Account', filters=filters)


def get_party(iban, payment_type):
	party = find_party(iban)
	return party 
