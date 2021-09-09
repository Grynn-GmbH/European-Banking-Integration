def Kreissparkasse_transformer(row):

	els = row

	return {
		'amount': create_amount(els[8]),
		'currency': els[9],
		'booking_date': create_date(els[1]),
		'iban': els[6],
		'bank_code': els[7],
		'comments': els[4],
		'payer': els[5],
		'reference_date': create_date(els[2]),
	}

def create_amount(amount):
	amount = amount.replace('"', '')
	if ',' not in amount:
		return int(amount)
	else:
		return float('.'.join(amount.split(',')))

def create_date(date):
	return '-'.join(date.split('.'))