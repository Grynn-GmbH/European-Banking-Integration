import frappe
import csv
from frappe.utils import get_site_name
from european_banking_integration.utils import get_file_path, get_party, get_paid_from, account_paid_to
from os import path
from european_banking_integration.reader import Reader
from european_banking_integration.transformer import Kreissparkasse_transformer

	file_path  = get_file_path(doc.import_file)

