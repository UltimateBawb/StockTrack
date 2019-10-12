import psycopg2
from queue import Queue
import multiprocessing as mp
import yfinance as yf

def get_and_commit(symbol, running):
	db_con = psycopg2.connect(host = "localhost", database = "postgres", user = "postgres", password = "postgres")
	db_cur = None

	try:
		ticker = yf.Ticker(symbol)
		hist = ticker.history(period = "max")

		db_cur = db_con.cursor()
		for t in hist.itertuples():
			stmt = "INSERT INTO prices (symbol, day, open, close, high, low, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
			tupl = (symbol, t.Index, t.Open, t.Close, t.High, t.Low, t.Volume)
			db_cur.execute(stmt, tupl)
		db_con.commit()
	except Exception as e:
		if db_con.closed == 0:
			db_con.rollback()
		pass
	
	if db_cur is not None:
		db_cur.close()
	if db_con.closed == 0:
		db_con.close()

	print("Finished work on " + symbol)
	running.value -= 1

symbols = []
with open("nasdaqlisted.txt") as f:
	for l in f.readlines():
		symbols.append(l.split("|")[0])

to_run = Queue()
running = mp.Value('d', 0)

for symbol in symbols:
	to_run.put(symbol)

while not to_run.empty():
	if running.value < 80:
		running.value += 1
		
		p = mp.Process(target = get_and_commit, args = (to_run.get(), running,))
		p.start()