import frappe 

def on_install():
	"""
	Run on Install
	"""

	# Create Supplier
	supplier = frappe.new_doc('Supplier')
	supplier.supplier_name = 'Temp Supplier'
	supplier.supplier_group = 'All Supplier Groups'
	supplier.insert()
	

	# Create Customer
	customer = frappe.new_doc('Customer')
	customer.full_name = 'Temp Customer'
	customer.insert()
	pass