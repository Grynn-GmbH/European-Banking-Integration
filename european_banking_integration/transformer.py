def Kreissparkasse_transformer(row):

	return {
		'amount': create_amount(row[8]),
		'currency': row[9],
		'booking_date': create_date(row[1]),
		'iban': row[6],
		'bank_code': row[7],
		'comments': row[4],
		'payer': row[5],
		'reference_date': create_date(row[2]),
	}

def create_amount(amount):
	amount = amount.replace('"', '')
	if ',' not in amount:
		return int(amount)
	else:
		return float('.'.join(amount.split(',')))

def create_date(date):
	return '-'.join(date.split('.'))