"""
@ CSU0018 Computer Algorithms
@ Programming Assignment 01
@ Convex Hull - Brute Force
"""
import sys
SAMPLE_NO = 1 #sys.argv[1]

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

def list2points(lst):
	return [Point(x, y, i) for (i, (x, y)) in enumerate(lst, 1)]

def convex_hull_brute_force(points):
	points = list2points(points)
	vertices = []
	import itertools
	for (point1, point2) in itertools.combinations(points, 2):
		if point1['x'] == point2['x'] and point1['y'] == point2['y']:
			continue
		L = Line(point1, point2)
		pos, neg = 0, 0
		for point in points:
			if L.value(point) > 0:
				pos += 1
			elif L.value(point) < 0:
				neg += 1
		if pos == 0 or neg == 0:
			vertices += [point1, point2]
	vertices = list(set(vertices))
	vertices.sort(key = lambda p : p['i'])
	return vertices

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

	ret = convex_hull_brute_force(input_data)

	finish = clock()
	print((finish - start))
	
	f_output = open('sample' + str(SAMPLE_NO) + '_BFout.txt', 'w')
	f_output.write(str(len(ret)) + '\n')
	for p in ret:
		f_output.writelines(str(p['i']) + '\n')
#	print(len(ret))
#	for p in ret:
#		print(p['i'])