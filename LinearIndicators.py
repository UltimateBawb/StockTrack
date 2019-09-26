import DBManager

def find_trend(symbol, start_date, end_date):
	records = DBManager.get_records(symbol, start_date, end_date)

	# WIP TODO
	for record in records:
		print("Date: " + record[1].strftime("%Y-%m-%d") + "; High: " + str(record[4]) + "; Low: " + str(record[5]))

find_trend("AMD", "2001-01-01", "2002-01-01")