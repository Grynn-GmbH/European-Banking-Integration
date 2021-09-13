def Kreissparkasse_transformer(row):

	return {
		'amount': create_amount(row[8]),
		'currency': row[9],
		'booking_date': create_date(row[1]),
		'iban': row[6],
		'bank_code': row[7],
		'comments': row[4],
		'payer': row[5],
		'reference': "{}\n{}\n{}".format(row[3], row[4], row[5]),
		'reference_date': create_date(row[2]),
	}

def create_amount(amount):
	amount = amount.replace('"', '')
	if ',' not in amount:
		return int(amount)
	else:
		return float('.'.join(amount.split(',')))

def create_date(date):
	dt = date.split('.')
	month = dt[1]
	day = dt[0]
	year = "20{}".format(dt[2])
	ref_dt = "{}-{}-{}".format(year, month, day)
	return ref_dt