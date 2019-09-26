import psycopg2

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# start_date, end_date format YYYY-MM-DD
def get_records(symbol, start_date, end_date):
	db_con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
	db_cur = db_con.cursor()

	stmt = "SELECT * FROM prices WHERE symbol = %s AND day BETWEEN date %s and date %s"
	tupl = (symbol, start_date, end_date)
	db_cur.execute(stmt, tupl)

	records = []
	for db_rec in db_cur:
		records.append(db_rec)

	if db_cur is not None:
		db_cur.close()

	if db_con.closed == 0:
		db_con.close()

	return records