import frappe

def find_supplier(iban):
	bank_account = frappe.get_list(
		'Bank Account', filters=[['iban', '=', iban], ["party_type", "=", "Supplier"]])
		
	if len(bank_account) > 0:
		return frappe.get_doc('Bank Account', bank_account[0])
	else:
		return False

def find_customer(iban):
	"""
	Find Supplier
	
	"""
	bank_account = frappe.get_list('Bank Account', filters=[['iban', '=', iban], ["party_type", "=", "Customer"]])	

	if len(bank_account) > 0:
		return frappe.get_doc('Bank Account', bank_account[0])
	else:
		return False

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
		["account_type", "in", ["bank", "Payable"]]
	]
	return frappe.db.get_list('Account', filters=filters)


def get_party(doc):
	supplier = find_supplier(doc.iban)
	customer = find_customer(doc.iban)

	if supplier:
		return ['Supplier', supplier.name, supplier.name ]
	elif customer(doc.iban):
		return ['Customer',  customer.name, customer.name]
	else:
		return [False, False, False]
