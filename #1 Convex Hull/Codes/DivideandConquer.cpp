#include <cstdio>
#include <algorithm>
#include <vector>
#include <cmath>
#include <limits>

class Point{
public:
	Point(long long x, long long y, int i = 0) : _x(x), _y(y), _i(i) {}
	long long x(void) const { return _x; }
	long long y(void) const { return _y; }
	int index(void) const { return _i; }
	bool operator<(const Point &q) const { return _x < q.x(); }
	bool operator==(const Point &q) const { return _x == q.x() && _y == q.y() && _i == q.index(); }
private:
	long long _x;
	long long _y;
	int _i;
};

class Line{
public:
	Line(Point &p, Point &q) : _p(p), _q(q) { build(); }
	long long value(Point &p) const { return _a * p.x() + _b * p.y() + _c; }
	double distance(Point &p) const { return static_cast<double>(std::abs(value(p))) / std::sqrt(_a * _a + _b * _b); }
private:
	void build(void) { _a = _q.y() - _p.y(); _b = _p.x() - _q.x(); _c = -(_a * _p.x() + _b * _p.y()); }
	Point &_p;
	Point &_q;
	long long _a;
	long long _b;
	long long _c;
};

class Triangle{
public:
	Triangle(Point left, Point right, Point top) : _l(left), _r(right), _t(top), _left(Line(left, top)), _right(Line(right, top)) { build(); }
	double area(void) const { return _area; }
	// return line of sides
	Line left(void) const { return _left; }
	Line right(void) const { return _right; }
	// return vertices
	Point l_vertex(void) const { return _l; }
	Point r_vertex(void) const { return _r; }
	Point t_vertex(void) const { return _t; }
	bool isInside(Point &d) const { return Triangle(_t, _l, d).area() + Triangle(_t, _r, d).area() + Triangle(_l, _r, d).area() == _area; }
private:
	void build(void) { _area = 0.5 * static_cast<double>(std::abs((_r.x()-_l.x()) * (_t.y()-_l.y()) - (_t.x()-_l.x()) * (_r.y()-_l.y()))); }
	Point _l;
	Point _r;
	Point _t;
	Line _left;
	Line _right;
	double _area;
};

// pre- and post-operation
void convex_hull(std::vector<Point> &points);
// called by convex_hull
std::vector<Point> divide_and_conquer(Triangle triangle, std::vector<Point> &points);

int main(int argc, char const *argv[]) {
	int rows;
	while(scanf("%d", &rows) != EOF) {
		std::vector<Point> points;
		points.reserve(rows * sizeof(points));
		for(int i = 1; i <= rows; ++i) {
			long long x, y;
			scanf("%lld %lld", &x, &y);
			points.push_back(Point(x, y, i));
		}
		convex_hull(points);
	}
	return 0;
}

std::vector<Point> divide_and_conquer(Triangle triangle, std::vector<Point> &points) {
	std::vector<Point> ret;
	std::vector<Point> l_points;
	std::vector<Point> r_points;
	std::vector<Point> l_line;
	std::vector<Point> r_line;
	double l_max_dist = -std::numeric_limits<double>::infinity();
	double r_max_dist = -std::numeric_limits<double>::infinity();
	Point l_max_point(0, 0);
	Point r_max_point(0, 0);
	double dist;
	for(auto &point : points) {
		if(triangle.left().value(point) == 0)				// point is on the left side
			l_line.push_back(point);
		else if(triangle.right().value(point) == 0)			// point is on the right side
			r_line.push_back(point);
		else if(triangle.isInside(point))					// point is inside the triangle
			continue;
		else if(point.x() < triangle.t_vertex().x()) {	// point is in the left
			l_points.push_back(point);
			dist = triangle.left().distance(point);
			if(dist > l_max_dist) {
				l_max_dist = dist;
				l_max_point = point;
			}
		}
		else if(point.x() > triangle.t_vertex().x()) {	// point is in the right
			r_points.push_back(point);
			dist = triangle.right().distance(point);
			if(dist > r_max_dist) {
				r_max_dist = dist;
				r_max_point = point;
			}
		}
	}
	if(l_points.size() > 0) {			// left side has point(s), divide.
		ret.push_back(l_max_point);
		std::vector<Point> l_hull = divide_and_conquer(Triangle(triangle.l_vertex(), triangle.t_vertex(), l_max_point), l_points);
		ret.insert(ret.end(), l_hull.begin(), l_hull.end());
	}
	else
		ret.insert(ret.end(), l_line.begin(), l_line.end());
	if(r_points.size() > 0) {			// right side has point(s), divide.
		ret.push_back(r_max_point);
		std::vector<Point> r_hull = divide_and_conquer(Triangle(triangle.t_vertex(), triangle.r_vertex(), r_max_point), r_points);
		ret.insert(ret.end(), r_hull.begin(), r_hull.end());
	}
	else
		ret.insert(ret.end(), r_line.begin(), r_line.end());

	return ret;
}

void convex_hull(std::vector<Point> &points) {
	// sort points by x
	std::sort(points.begin(), points.end());
	// points to return
	std::vector<Point> ret;

	Point pointL = points.front();
	Point pointR = points.back();
	ret.push_back(pointL);
	ret.push_back(pointR);
	// Line of points has max and min x.
	Line L(pointL, pointR);

	// points in positive or negative side of L
	std::vector<Point> pos;
	std::vector<Point> neg;

	// max distances and points in both sides.
	double pos_max_dist = -std::numeric_limits<double>::infinity();
	double neg_max_dist = -std::numeric_limits<double>::infinity();
	Point pos_max_point(0, 0);
	Point neg_max_point(0, 0);

	for(auto &point : points) {
		double dist = L.distance(point);
		if(L.value(point) > 0) {
			pos.push_back(point);
			if(dist > pos_max_dist) {
				pos_max_dist = dist;
				pos_max_point = point;
			}
		}
		else if(L.value(point) < 0) {
			neg.push_back(point);
			if(dist > neg_max_dist) {
				neg_max_dist = dist;
				neg_max_point = point;
			}
		}
	}

	//if pos or neg side has any points, divide.
	if(pos.size() > 0) {
		ret.push_back(pos_max_point);
		std::vector<Point> pos_hull = divide_and_conquer(Triangle(pointL, pointR, pos_max_point), pos);
		ret.insert(ret.end(), pos_hull.begin(), pos_hull.end());
	}
	if(neg.size() > 0) {				// if neg side has any points, divide.
		ret.push_back(neg_max_point);
		std::vector<Point> neg_hull = divide_and_conquer(Triangle(pointL, pointR, neg_max_point), neg);
		ret.insert(ret.end(), neg_hull.begin(), neg_hull.end());
	}
	std::sort(ret.begin(), ret.end(), [&](Point p, Point q) { return p.index() < q.index(); });	// sort by index
	ret.erase(std::unique(ret.begin(), ret.end()), ret.end());	// make indecies unique.

	// output
	printf("%d\n", (int)ret.size());
	for(auto i : ret)
		printf("%d\n", i.index());
}