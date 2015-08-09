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
	int index(void) const {return _i; }
	bool operator<(const Point &q) const { return (_x == q.x()) ? _y < q.y() : _x < q.x(); }
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

// main operation
void convex_hull(std::vector<Point> &points);

int main(int argc, char const *argv[]) {
	int rows;
	while(scanf("%d", &rows) != EOF) {
		std::vector<Point> points;
		points.reserve(rows * sizeof(points));
		for(int i = 1; i <= rows; ++i) {
			long long x, y;
			scanf("%I64d %I64d", &x, &y);
			points.push_back(Point(x, y, i));
		}
		convex_hull(points);
	}
	return 0;
}

void convex_hull(std::vector<Point> &points) {
	std::sort(points.begin(), points.end());
	std::vector<Point> ret;

	while (true) {
		Line L(points[0], points[1]);
		int pos = 0;
		int neg = 0;
		for (auto &point : points) {
			if(L.value(point) > 0)
				pos += 1;
			else if(L.value(point) < 0)
				neg += 1;
		}
		if(pos == 0 || neg == 0) {
			ret.push_back(points[0]);
			ret.push_back(points[1]);
		}
		std::prev_permutation(points.begin() + 2, points.end());
		if (!std::next_permutation(points.begin(), points.end()))
			break;
	}
	
	std::sort(ret.begin(), ret.end(), [&](Point p, Point q) { return p.index() < q.index(); });
	ret.erase(std::unique(ret.begin(), ret.end()), ret.end());
	printf("%d\n", ret.size());
	for(auto &i : ret)
		printf("%d\n", i.index());
}