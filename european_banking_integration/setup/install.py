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
	supplier.save()
	

	# Create Customer
	customer = frappe.new_doc('Customer')
	customer.customer_name = 'Temp Customer'
	customer.customer_group = 'All Customer Groups'
	customer.territory = 'All Territories'
	customer.insert()
	customer.save()

	