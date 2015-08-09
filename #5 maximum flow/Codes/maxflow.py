"""
CSU0018 Computer Algorithms
Programming Assignment 05
Maximum Flow
"""

def edmonds_karp(graph, weight, s, t):
	max_flow, flow_table = 0, {edge : 0 for edge in weight}
	while True:
		rd_graph, rd_weight = make_residual(graph, weight, flow_table)
		augment_path, augment_flow = find_augment_path(rd_graph, rd_weight, s, t)
		if not augment_path:
			break
		max_flow += augment_flow
		for edge in augment_path:
			if edge in flow_table:
				flow_table[edge] += augment_flow
			else:
				flow_table[(edge[1], edge[0])] -= augment_flow

	return max_flow

def find_augment_path(rd_graph, rd_weight, s, t):
	shortest_path = BFS_shortest_path(rd_graph, s, t)
	flow = 0
	if shortest_path:
		flow = min([rd_weight[edge] for edge in shortest_path])
	return shortest_path, flow

def make_residual(graph, weight, flow_table):
	rd_graph, rd_weight = {p : [] for p in graph}, {}

	for edge in flow_table:
		if flow_table[edge]:
			rd_graph[edge[1]].append(edge[0])
			rd_weight[(edge[1], edge[0])] = flow_table[edge]
	for edge in weight:
		if weight[edge] > flow_table[edge]:
			rd_graph[edge[0]].append(edge[1])
			rd_weight[edge] = weight[edge] - flow_table[edge]
	return rd_graph, rd_weight

def BFS_shortest_path(graph, s, t):
	iterated, pred, q = set(), {p : '' for p in graph}, [s]
	while len(q) != 0:
		last = q.pop(0)
		for v in graph[last]:
			if not v in iterated:
				q.append(v)
				iterated.add(v)
				pred[v] = last
	pred[s] = ''

	path, cur_pt = [], t
	while pred[cur_pt]:
		path.append((pred[cur_pt], cur_pt))
		cur_pt = pred[cur_pt]
	return path

####################################################################################
SAMPLE_NO = 2

if __name__ == '__main__':
	lines = [line.strip('\n').split() for line in open("test" + str(SAMPLE_NO) + ".txt")]
	s, t = map(lambda x: int(x), lines[1])
	graph, weight = {v : [] for v in range(1, int(lines[0][0]) + 1)}, {}

	for line in lines[2:]:
		w, u, v = map(lambda x: int(x), line)
		if (u, v) in weight:
			weight[(u, v)] += w
		else:
			weight[(u, v)] = w
		graph[u].append(v)
	print(edmonds_karp(graph, weight, s, t))