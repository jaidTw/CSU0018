"""
@ CSU0018 Computer Algorithms
@ Programming Assignment 01
@ Convex Hull
"""

import random

# set PLOT to True to enable plotting features.
# must install matplotlib.
PLOT = True
# RANGE OF X AND Y OF POINTS
RANGE = 1000
# DATA
DATA = 100


if PLOT:
	import matplotlib.pyplot
	matplotlib.pyplot.xlim(RANGE * -.1, RANGE * 1.1)
	matplotlib.pyplot.ylim(RANGE * -.1, RANGE * 1.1)
# Utilities
class Point:
	def __init__(self, x, y, i):
		self._x = x
		self._y = y
		self._i = i

	def __getitem__(self, coord):
		if coord == "x":
			return self._x
		elif coord == "y":
			return self._y
		elif coord == "i":
			return self._i
		else:
			assert()

	if PLOT:
		def plot(self):	matplotlib.pyplot.plot(self._x, self._y, "o")

class Line:
	def __init__(self, p, q):
		self._a = q["y"] - p["y"]
		self._b = p["x"] - q["x"]
		self._c = -(self._a * p["x"] + self._b * p["y"])
		self._p = p
		self._q = q

	def distance(self, point):
		return abs(self.value(point))/(self._a**2 + self._b**2)**0.5

	def value(self, point):
		return self._a * point["x"] + self._b * point["y"] + self._c

	if PLOT:
		def plot(self):
			matplotlib.pyplot.plot([self._p["x"], self._q["x"]], [self._p["y"], self._q["y"]], "b--", linewidth = 2)

class Triangle:
	def __init__(self, left, right, top):
		self._l = left
		self._r = right
		self._t = top
		self._area = 0.5*abs((right['x']-left['x'])*(top['y']-left['y'])\
						 - (top['x']-left['x'])*(right['y']-left['y']))
		self._left = Line(left, top)
		self._right = Line(right, top)

	def inside(self, d):
		return Triangle(self._t, self._l, d)._area + Triangle(self._t, self._r, d)._area + Triangle(self._l, self._r, d)._area == self._area

	if PLOT:
		def plot(self):
			self._t.plot()
			self._l.plot()
			self._r.plot()
			self._left.plot()
			self._right.plot()

	def __getitem__(self, str):
		if str == 't':
			return self._t
		elif str == 'l':
			return self._l
		elif str == 'r':
			return self._r
		elif str == 'left':
			return self._left
		elif str == 'right':
			return self._right

def list2points(lst):
	return [Point(x, y, i) for (i, (x, y)) in enumerate(lst, 1)]

#main function
def convex_hull_divide_and_conquer(points):
	def div_conq(triangle, points):
		ret = []
		l_max_dist, r_max_dist = [float('-inf'), 0], [float('-inf'), 0]
		l_points, r_points = [], []
		l_line, r_line = [], []
		for point in points:
			if triangle.inside(point):
				continue
			elif triangle['left'].value(point) == 0:
				l_line.append(point)
			elif triangle['right'].value(point) == 0:
				r_line.append(point)
			elif point['x'] < triangle['t']['x']:
				l_points.append(point)
				dist = triangle['left'].distance(point)
				if  dist > l_max_dist[0]:
					l_max_dist = dist, point
			elif point['x'] > triangle['t']['x']:
				r_points.append(point)
				dist = triangle['right'].distance(point)
				if  dist > r_max_dist[0]:
					r_max_dist = dist, point

		if len(l_points) > 0:
			ret.append(l_max_dist[1])
			ret += div_conq(Triangle(triangle['l'], triangle['t'], l_max_dist[1]), l_points)
		else:
			if PLOT:
				triangle.plot()
			ret.extend(l_line)
		if len(r_points) > 0:
			ret.append(r_max_dist[1])
			ret += div_conq(Triangle(triangle['t'], triangle['r'], r_max_dist[1]), r_points)
		else:
			if PLOT:
				triangle.plot()
			ret.extend(r_line)
		return ret

	points = list2points(points)
	if PLOT:
		for point in points:
			point.plot()
	points.sort(key = lambda p : (p['x'],p['y']))

	ret = []
	pointL, pointR = points[0], points[-1]
	ret += [pointL, pointR]
	L = Line(pointL, pointR)

	pos, neg = [], []
	pos_max, neg_max = [float('-inf'), 0], [float('-inf'), 0]
	for point in points:
		dist = L.distance(point)
		if L.value(point) > 0:
			pos.append(point)
			if dist > pos_max[0]:
				pos_max = dist, point
		elif L.value(point) < 0:
			neg.append(point)
			if dist > neg_max[0]:
				neg_max = dist, point
	if len(pos) > 0:
		ret.append(pos_max[1])
		ret += div_conq(Triangle(pointL, pointR, pos_max[1]), pos)
	if len(neg) > 0:
		ret.append(neg_max[1])
		ret += div_conq(Triangle(pointL, pointR, neg_max[1]), neg)
	return list(set(ret))

def convex_hull_brute_force(points):
	points = list2points(points)
	if PLOT:
		for point in points:
			point.plot()
	vertices = []
	import itertools
	for (point1, point2) in itertools.combinations(points, 2):
		L = Line(point1, point2)
		pos, neg = 0, 0
		for point in points:
			if L.value(point) > 0:
				pos += 1
			elif L.value(point) < 0:
				neg += 1
		if pos == 0 or neg == 0:
			if PLOT:
				L.plot()
			vertices += [point1, point2]
	return list(set(vertices))

sample_input = []
for _ in range(DATA):
	sample_input.append((random.randrange(RANGE),random.randrange(RANGE)))
#sample_input = [(55, 6), (62, 13), (4, 77), (69, 60), (63, 12), (26, 27), (5, 43), (73, 71), (65, 26), (98, 91), (56, 71), (81, 88), (93, 16), (58, 13), (91, 45), (98, 63), (48, 83), (68, 68), (69, 68), (98, 88), (10, 40), (68, 12), (48, 80), (49, 54), (12, 68), (37, 49), (40, 0), (15, 93), (62, 6), (22, 8), (61, 94), (37, 89), (50, 21), (39, 82), (7, 4), (84, 79), (29, 56), (64, 30), (18, 70), (59, 1), (70, 43), (36, 11), (17, 5), (29, 99), (95, 71), (51, 33), (21, 80), (17, 59), (79, 0), (26, 59), (17, 78), (44, 28), (79, 14), (34, 40), (70, 35), (43, 89), (63, 91), (84, 67), (45, 92), (58, 68), (19, 58), (41, 58), (24, 20), (56, 11), (39, 25), (92, 63), (89, 1), (73, 62), (34, 51), (73, 38), (5, 98), (44, 70), (51, 89), (44, 83), (64, 2), (68, 69), (12, 67), (44, 47), (21, 82), (33, 39), (27, 87), (57, 42), (59, 0), (9, 44), (79, 76), (15, 88), (6, 49), (70, 43), (62, 83), (23, 19), (2, 52), (7, 72), (51, 82), (95, 82), (49, 95), (93, 14), (98, 72), (43, 74), (16, 27), (12, 67)]
#sample_input = [(1, 2), (2, 3), (2, 2), (3, 1), (3, 2)]
#sample_input = [(1, 1), (8, 8), (1, 8), (8, 1), (1, 2), (2, 1), (2, 8), (8, 2)]
#for _ in range(20):
#	p = (random.randrange(2, 8), random.randrange(2, 8))
#	if not p in sample_input:
#		sample_input.append(p)

#BF = convex_hull_brute_force(sample_input)
DC = convex_hull_divide_and_conquer(sample_input)
#BF.sort(key=lambda p: p['i'])
DC.sort(key=lambda p: p['i'])
#print([p['i'] for p in BF])
print([p['i'] for p in DC])

if PLOT:
	matplotlib.pyplot.show()