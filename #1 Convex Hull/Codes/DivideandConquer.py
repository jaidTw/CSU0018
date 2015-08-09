"""
@ CSU0018 Computer Algorithms
@ Programming Assignment 01
@ Convex Hull - Divide and Conquer
"""
import sys
SAMPLE_NO = sys.argv[1]

# Utilities
class Point:
	def __init__(self, x, y, i):
		self._x = x
		self._y = y
		self._i = i

	def __getitem__(self, coord):
		if coord == 'x':
			return self._x
		elif coord == 'y':
			return self._y
		elif coord == 'i':
			return self._i
		else:
			assert()

class Line:
	def __init__(self, p, q):
		self._a = q['y'] - p['y']
		self._b = p['x'] - q['x']
		self._c = -(self._a * p['x'] + self._b * p['y'])
		self._p = p
		self._q = q

	def distance(self, point):
		return abs(self.value(point))/(self._a**2 + self._b**2)**0.5

	def value(self, point):
		return self._a * point['x'] + self._b * point['y'] + self._c

class Triangle:
	def __init__(self, left, right, top):
		self._l = left
		self._r = right
		self._t = top
		self._area = 0.5*abs((right['x']-left['x'])*(top['y']-left['y']) \
						 - (top['x']-left['x'])*(right['y']-left['y']))
		self._buttom = Line(left, right)
		self._left = Line(left, top)
		self._right = Line(right, top)
		
	def inside(self, d):
		return Triangle(self._t, self._l, d)._area + \
					Triangle(self._t, self._r, d)._area + \
						Triangle(self._l, self._r, d)._area == self._area

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
			ret.extend(l_line)
		if len(r_points) > 0:
			ret.append(r_max_dist[1])
			ret += div_conq(Triangle(triangle['t'], triangle['r'], r_max_dist[1]), r_points)
		else:
			ret.extend(r_line)
		return ret


	points = list2points(points)
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

	ret = list(set(ret))
	ret.sort(key = lambda p : p['i'])
	return ret

if __name__ == '__main__':
	f_input = open('sample' + str(SAMPLE_NO) + '.txt', 'r')
	f_input.readline()
	input_data = []
	for line in f_input:
		line = line.strip('\n')
		x, y = line.split()
		input_data.append((int(x), int(y)))
	
	from time import clock
	start = clock()

	f_output = open('sample' + str(SAMPLE_NO) + '_DCout.txt', 'w')
	ret = convex_hull_divide_and_conquer(input_data)

	finish = clock()
	print((finish - start))

	f_output.write(str(len(ret)) + '\n')
	for p in ret:
		f_output.writelines(str(p['i']) + '\n')
#	print(len(ret))
#	for p in ret:
#		print(p['i'])