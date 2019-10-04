import DBManager
import itertools
import numpy as np

# Given a numpy array, return a new numpy array of all possible 2-combinations
def pairwise_combs(ab):
    n = len(ab)
    N = n*(n-1)//2
    out = np.empty((N,2,2),dtype=ab.dtype)
    idx = np.concatenate(( [0], np.arange(n-1,0,-1).cumsum() ))
    start, stop = idx[:-1], idx[1:]
    for j,i in enumerate(range(n-1)):
        out[start[j]:stop[j],0] = ab[j]
        out[start[j]:stop[j],1] = ab[j+1:]
    return out

def pair_range(p1, p2, points):
	for i in range(int(p1[0]), int(p2[0])):
		if (i != 0):
			yield(points[i])

def find_trend(symbol, start_date, end_date):
	records = DBManager.get_records(symbol, start_date, end_date)

	print(records[195])
	print(records[206])
	return

	points = []
	for idx, val in enumerate(records):
		point = np.array([idx, val[5]])
		points.append(point)

	# Create a numpy array of points and get all pairs
	points = np.asarray(points, dtype=np.float32)
	pairs = pairwise_combs(points)

	diffs = []
	for pair in pairs:
		p0 = pair[0]
		p1 = pair[1]
		v = p1 - p0
		
		diff_arr = []
		for p in pair_range(p0, p1, points):
			v = v * (p[0] / v[0]) + p0

			diff = p - v
			diff_p = diff[1] / p[1]

			diff_arr.append(diff_p)

		diffs.append([pair, diff_arr])
	
	i = 0
	for l in diffs:
		diff = l[1]
		loss = 0
		for v in diff:
			if v < 0:
				loss += v
		diffs[i].append(loss)
		i += 1

	diffs.sort(key = lambda x: x[2])

	i = len(diffs) - 1
	while i > (0):
		v = diffs[i]
		if (v[2] > -5 and v[0][1][0] - v[0][0][0]) > 10:
			print(diffs[i])

		i -= 1





	#cpair = pairs[5000]
	#for x in pair_range(cpair[0], cpair[1], points):
	#	print(x)

	
	#for i in range(int(cpair[0][0]), int(cpair[1][0])):
	#	print(points[i])


find_trend("AMD", "2018-01-01", "2019-01-01")