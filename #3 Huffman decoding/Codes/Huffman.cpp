/*
 * CSU0018 Computer Algorithms
 * Programming Assignment 03
 * Huffman Decoding - Greedy Algorithm
 */
#include <iostream>
#include <algorithm>
#include <string>
#include <unordered_map>
#include <deque>
#include <cstdio>

using namespace std;

typedef pair<string, double> prob_t;
inline string get_str(prob_t prob) { return get<0>(prob); }
inline double get_prob(prob_t prob) { return get<1>(prob); }

typedef pair<char, string> code_map;
inline char get_key(code_map map) { return get<0>(map); }
inline string get_code(code_map map) { return get<1>(map); }

inline string int2str(int i) { char tmp[8]; sprintf(tmp, "%d", i); return string(tmp); }
void huffman_decode(deque<prob_t>&, string&);

int main(void) {
	deque<prob_t> prob;
	string input;
	float p;
	int i = 0;
	while(cin >> p) {
		prob.push_back(make_pair(int2str(i), p));
		++i;
		if(i > 9) {
			cin.clear();
			cin >> input;
			huffman_decode(prob, input);
			i = 0;
			prob.clear();
		}
	}
	return 0;
}

void huffman_decode(deque<prob_t> &prob, string &encode_str) {
	unordered_map<char, string> table;
	for(auto i = '0'; i <= '9'; ++i)
		table[i] = "";
	
	while(prob.size() > 1) {
		sort(prob.begin(), prob.end(), [&](prob_t x, prob_t y) { return get_prob(x) < get_prob(y); });
		
		auto left = prob[0];
		prob.pop_front();
		auto right = prob[0];
		prob.pop_front();

		for(size_t i = 0; i < get_str(left).length(); ++i)
			table[get_str(left)[i]] = "1" + table[get_str(left)[i]];
		for(size_t i = 0; i < get_str(right).length(); ++i)
			table[get_str(right)[i]] = "0" + table[get_str(right)[i]];

		prob.push_back(make_pair(get_str(left) + get_str(right), get_prob(left) + get_prob(right)));
	}

	string result = "";
	while(encode_str.length() != 0) {
		for(auto &item : table) {
			string code = get_code(item);
			string sub = encode_str.substr(0, get_code(item).length());
			if(code == sub) {
				result += get_key(item);
				encode_str = encode_str.substr(code.length());
			}
		}
	}
	cout << result;
}