/*
 * CSU0018 Computer Algorithms
 * Programming Assignment 05
 * Maximum Flow
 */
 
#include <cstdio>
#include <vector>
#include <list>
#include <unordered_map>
#include <algorithm>
#include "tuple_hash.h"

using namespace std;

typedef unsigned int point_t;
typedef unsigned int weight_t;
typedef unsigned int flow_t;
typedef vector<vector<point_t>> graph_t;
typedef tuple<point_t, point_t> edge_t;
typedef vector<edge_t> path_t;
typedef unordered_map<point_t, point_t> predecessor_table_t;
typedef unordered_map<edge_t, weight_t> weight_table_t;

flow_t ford_fulkerson(graph_t &, weight_table_t &, point_t, point_t);
tuple<path_t, flow_t> find_augment_path(graph_t &, weight_table_t &, point_t, point_t);
tuple<graph_t, weight_table_t> make_residual(graph_t &, weight_table_t &, weight_table_t &);
path_t BFS_shortest_path(graph_t &, point_t, point_t);

static size_t num_of_vertices, num_of_edges;

int main(void) {
	while(scanf("%u %u", &num_of_vertices, &num_of_edges) != EOF) {
		point_t s, t;
		scanf("%u %u", &s, &t);

		graph_t graph(num_of_vertices + 1);
		weight_table_t weight;
		for(size_t i = 0; i < num_of_edges; ++i) {
			weight_t w;
			point_t u, v;
			scanf("%u %u %u", &w, &u, &v);

			if(weight.find(make_tuple(u, v)) != weight.end())
				weight[make_tuple(u, v)] += w;
			else
					weight[make_tuple(u, v)] = w;
			graph[u].push_back(v);
		}
		printf("%u", ford_fulkerson(graph, weight, s, t));
	}
	return 0;
}


flow_t ford_fulkerson(graph_t &graph, weight_table_t &weight, point_t s, point_t t) {
	int max_flow = 0;
	weight_table_t flow_table;
	while(true) {
		graph_t rd_graph;
		weight_table_t rd_weight;
		tie(rd_graph, rd_weight) = make_residual(graph, weight, flow_table);
		
		path_t augment_path;
		flow_t augment_flow;
		tie(augment_path, augment_flow) = find_augment_path(rd_graph, rd_weight, s, t);
		if(augment_path.empty())
			break;
		max_flow += augment_flow;
		for(auto &edge : augment_path)
			if(flow_table.find(edge) != flow_table.end())
				flow_table[edge] += augment_flow;
			else
				flow_table[make_tuple(get<1>(edge), get<0>(edge))] -= augment_flow;
	}
	return max_flow;
}

tuple<path_t, flow_t> find_augment_path(graph_t &rd_graph, weight_table_t &rd_flow, point_t s, point_t t) {
	// Edmonds Karp Stragegy
	path_t shortest_path = BFS_shortest_path(rd_graph, s, t);
	flow_t flow = 0;
	if(!shortest_path.empty())
		flow = rd_flow[*min_element(shortest_path.begin(), shortest_path.end(), [&](edge_t eA, edge_t eB) { return rd_flow[eA] < rd_flow[eB]; })];
	return make_tuple(shortest_path, flow);
}

tuple<graph_t, weight_table_t> make_residual(graph_t &graph, weight_table_t &weight, weight_table_t &flow_table) {
	graph_t rd_graph(num_of_vertices + 1);
	weight_table_t rd_weight;
	for(auto &p : flow_table) {
		auto &edge = get<0>(p);
		if(get<1>(p)) {
			rd_graph[get<1>(edge)].push_back(get<0>(edge));
			rd_weight[make_tuple(get<1>(edge), get<0>(edge))] = flow_table[edge];
		}
	}
	for(auto &p : weight) {
		auto &edge = get<0>(p);
		if(weight[edge] > flow_table[edge]) {
			rd_graph[get<0>(edge)].push_back(get<1>(edge));
			rd_weight[edge] = weight[edge] - flow_table[edge];
		}
	}
	return make_tuple(rd_graph, rd_weight);
}

path_t BFS_shortest_path(graph_t &graph, point_t s, point_t t) {
	predecessor_table_t predecessor;
	unordered_map<point_t, bool> visited;
	vector<point_t> point_vec = {s};

	while(!point_vec.empty()) {
		point_t last = *point_vec.rbegin();
		point_vec.pop_back();
		for(auto &v : graph[last])
			if(!visited[v]) {
				point_vec.push_back(v);
				visited[v] = true;
				predecessor[v] = last;
			}
	}
	predecessor[s] = 0;
	path_t shortest_path = {};
	point_t cur_point = t;
	while(predecessor[cur_point]) {
		shortest_path.push_back(make_tuple(predecessor[cur_point], cur_point));
		cur_point = predecessor[cur_point];
	}
	return shortest_path;
}