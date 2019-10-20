import DBManager
import itertools
import multiprocessing as mp
import numpy as np
import time

from functools import reduce
from queue import Queue

# Given a numpy array, return a new numpy array of all possible 2-combinations
# ab: The numpy array
def pairwise_combs(ab):
    n = len(ab)
    N = n * (n - 1) // 2

    out = np.empty((N, 2, 2),dtype = ab.dtype)
    idx = np.concatenate(([0], np.arange(n-  1, 0, -1).cumsum()))
    start, stop = idx[:-1], idx[1:]

    for j, i in enumerate(range(n-1)):
        out[start[j]:stop[j], 0] = ab[j]
        out[start[j]:stop[j], 1] = ab[(j + 1):]

    return out

# Given points p1 and p2 from a list of points, return all points between them
# p1: First point (2-dimension numpy array)
# p2: Second point (2-dimension numpy array)
# points: List of points in which p1 and p2 reside (numpy array of 2-dimension arrays)
def pair_range(p1, p2, points):
	for i in range(int(p1[0]) + 1, int(p2[0])):
		if (i != 0):
			yield(points[i])

# Given a difference percentage, calculate and return its loss value
# x: Percent difference (float)
def loss_func(x):
	if x >= 0:
		tmp = x + 0.7
		return np.power((-3 / (np.log2(tmp) - np.power(tmp, 2))), 4)

	return 2 * np.power(((x * 100) - 2), 5)

# Find all valid trend vectors in the date range for the given symbol
# symbol: The ticker symbol
# start_date: First date to consider (YYYY-MM-DD string)
# end_date: Last date to consider (YYYY-MM-DD string)
# type: Which portion of the record to use (record index int, e.g. 5 = daily min)
#	See prices table format
# min_distance: The minimum distance between a points to consider it for a trend vector (int)
def find_trend(symbol, start_date, end_date, type, min_distance, running, all_diffs):
	print("Finding trends for " + symbol)

	# Get all requested records from DB
	records = DBManager.get_records(symbol, start_date, end_date)

	# Get points from records depending on type parameter
	points = []
	for idx, val in enumerate(records):
		point = np.array([idx, val[type]])
		points.append(point)

	if len(points) == 0:
		return []

	# Create a numpy array of points and get all pairs
	points = np.asarray(points, dtype = np.float32)
	pairs = pairwise_combs(points)

	# Last point
	lp = points[len(points) - 1]

	diffs = []

	# Iterate all pairs
	for pair in pairs:
		p0 = pair[0]
		p1 = pair[1]

		# Lazy way to enforce min_distance
		if p1[0] - p0[0] < min_distance:
			continue

		# Trend vector to test
		v = p1 - p0

		diff_arr = []

		# Iterate all points between p0 and lp
		for p in pair_range(p0, lp, points):

			# Get the point where p is projected onto v
			v_mod = np.array((p[0], p0[1] + v[1] * (p[0] - p0[0]) / v[0]))

			# Find the percent distance from p
			diff = p - v_mod
			diff_p = diff[1] / p[1]

			diff_arr.append(diff_p)

		losses = list(map(loss_func, diff_arr))
		total_loss = reduce((lambda a, b: a + b), losses)

		# Get actual dates from pair info
		date0 = records[pair[0][0].astype(int)][1]
		date1 = records[pair[1][0].astype(int)][1]

		if (total_loss > 0):
			diffs.append([symbol, [date0, date1], total_loss])

	print("Finished LinearIndicators for " + symbol)
	all_diffs.extend(diffs)

	running.value -= 1

	#return diffs

to_run = Queue()
running = mp.Value('d', 0)

i = 0
symbols = DBManager.get_symbols()
for symbol in symbols:
	if i > 10000:
		break
	to_run.put(symbol)
	i += 1

all_diffs = []
with mp.Manager() as manager:
	l = manager.list()

	while not to_run.empty():
		if running.value < 8:
			p = mp.Process(target = find_trend, args = (to_run.get(), "2018-10-01", "2019-10-02", 5, 10, running, l,))
			p.start()
			running.value += 1

	# Wait for the last processes to finish
	#while running.value > 1:
	#	continue


	all_diffs.extend(l)
	print(len(all_diffs))
	all_diffs.sort(key = lambda x: x[2])
	all_diffs.reverse()

	print(all_diffs[:10])

# Get all support vectors
#vectors = find_trend("AMD", "2019-08-01", "2019-09-19", 5, 10)

# Print the best 10 results
#print(vectors[:10])