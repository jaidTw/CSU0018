/*
 * CSU0018 Computer Algorithms
 * Programming Assignment 02
 * LCS (continuous) - Dynamic Programming
 */
#include <iostream>
#include <string>
#include <cstdio>
#include <unordered_map>
#include <unordered_set>

inline size_t min(size_t a, size_t b) { return (a > b) ? b : a; }

void DP_print_LCS(std::string &str_a, std::string &str_b);

int main(int argc, char const *argv[]) {
	int n, m;
	while(scanf("%d %d", &n, &m) != EOF) {
		std::string str_a, str_b;
		std::cin >> str_a >> str_b;
		DP_print_LCS(str_a, str_b);
	}
	return 0;
}

void DP_print_LCS(std::string &str_a, std::string &str_b) {
	std::unordered_map<size_t, std::unordered_set<size_t>> sub_map;

	for(size_t a_idx = 0; a_idx < str_a.size(); ++a_idx)		// Fill map with sub string length = 1
		for(size_t b_idx = 0; b_idx < str_b.size(); ++b_idx)
			if(str_a[a_idx] == str_b[b_idx]) {
				if(sub_map.find(a_idx) == sub_map.end()) {
					std::unordered_set<size_t> idx_vec = { b_idx };
					sub_map.insert(std::make_pair(a_idx, idx_vec));
				}
				else
					sub_map[a_idx].emplace(b_idx);
			}

	std::string last = "";
	for(size_t sub_len = 1; sub_len < min(str_a.size(), str_b.size()); ++sub_len) {		// Eliminate
		std::unordered_set<size_t> pop_set;
		for(auto &pair : sub_map) {
			size_t a_idx = pair.first;
			if(a_idx + sub_len > str_a.size()) {
				pop_set.emplace(a_idx);
				continue;
			}

			std::unordered_set<size_t> remove_set;
			auto &idx_set = pair.second;
			for(auto b_idx : idx_set) {
				if(b_idx + sub_len > str_b.size()) {
					remove_set.emplace(b_idx);
					continue;
				}
				std::string a_tmp(str_a, a_idx, sub_len);
				std::string b_tmp(str_b, b_idx, sub_len);
				if(a_tmp != b_tmp)
					remove_set.emplace(b_idx);
				else
					last = a_tmp;
			}
			for(auto key : remove_set)
				idx_set.erase(key);
		}
		for(auto key : pop_set)
			sub_map.erase(key);
	}
	std::cout << last;
}