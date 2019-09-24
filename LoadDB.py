import yfinance as yf
import psycopg2
import threading
from queue import Queue

class glob_q():
	to_run = Queue()
	running = 0

def get_and_commit(symbol, con):
	db_cur = None
	try:
		ticker = yf.Ticker(symbol)
		hist = ticker.history(period = "max")

		db_cur = con.cursor()
		for t in hist.itertuples():
			stmt = "INSERT INTO prices (symbol, day, open, close, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
			tupl = (symbol, t.Index, t.Open, t.Close, t.High, t.Low, t.Volume)
			db_cur.execute(stmt, tupl)
		con.commit()
	except Exception as e:
		if con.closed == 0:
			con.rollback()
		pass
	
	if db_cur is not None:
		db_cur.close()
	if con.closed == 0:
		con.close()

	print("Finished work on " + symbol)
	glob_q.running -= 1

symbols = []
with open("nasdaqlisted.txt") as f:
	for l in f.readlines():
		symbols.append(l.split("|")[0])

for symbol in symbols:
	glob_q.to_run.put(symbol)

while not glob_q.to_run.empty():
	if glob_q.running < 80:
		glob_q.running += 1

		db_con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres")
		t = threading.Thread(target = get_and_commit, args = (glob_q.to_run.get(), db_con,))
		t.start()