/*
 * CSU0018 Computer Algorithms
 * Programming Assignment 04
 * The Box Problem
 */
#include <iostream>
#include <unordered_map>
#include <vector>
#include <algorithm>

class Box {
public:
	Box(int H, int W, int D, int i = 0) {
		std::vector<int> sides = {H, W, D};
		std::sort(sides.begin(), sides.end());
		_H = sides[0];
		_W = sides[1];
		_D = sides[2];
		vol = _H * _W * _D;
		NO = i;
	}
	bool can_contain(Box box) { return _H > box._H && _W > box._W && _D > box._D; }
	int vol;
	int NO;
private:
	int _H;
	int _W;
	int _D;
};

void max_boxing(std::vector<Box> &);

int main(void) {
	int lines;
	while(std::cin >> lines) {
		std::vector<Box> boxes;
		for(int i = 0; i < lines; ++i) {
			int h, w, d;
			std::cin >> h >> w >> d;
			boxes.push_back(Box(h, w, d, i));
		}
		max_boxing(boxes);
	}
	return 0;
}

void max_boxing(std::vector<Box> &boxes) {
	std::sort(boxes.begin(), boxes.end(), [&](Box a, Box b){ return a.vol < b.vol; });

	std::unordered_map<int, std::vector<Box>> adj_lst;
	for(size_t i = 0; i < boxes.size(); ++i) {
		std::vector<Box> adj;
		for(auto iter = boxes.begin() + i; iter != boxes.end(); ++iter)
			if((*iter).can_contain(boxes[i]))
				adj.push_back(*iter);
		adj_lst[boxes[i].NO] = adj;
	}

	std::unordered_map<int, int> depth_table;
	for(auto &box : boxes)
		depth_table[box.NO] = 1;

	int max_depth = 0;
	for(auto &box : boxes) {
		for(auto &adj : adj_lst[box.NO]) {
			int depth = depth_table[box.NO] + 1;
			if(max_depth < depth)
				max_depth = depth;
			if(depth_table[adj.NO] < depth)
				depth_table[adj.NO] = depth;
		}
	}

	std::cout << max_depth;
}