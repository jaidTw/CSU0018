"""
CSU0018 Computer Algorithms
Programming Assignment 03
Huffman Decoding - Greedy Algorithm
"""
def huffman_decode(prob_lst, encode_str):
	prob_lst = list(zip([str(x) for x in range(10)], prob_lst))
	table = {str(x) : "" for x in range(10)}
	
	while len(prob_lst) > 1:
		prob_lst.sort(key = lambda k: k[1])
		left = prob_lst.pop(0)
		right = prob_lst.pop(0)
		for char in left[0]:
			table[char] = "1" + table[char]
		for char in right[0]:
			table[char] = "0" + table[char]
		prob_lst.append((left[0] + right[0], left[1] + right[1]))
	result = ""
	while len(encode_str) != 0:
		for (key, code) in table.items():
			if encode_str[:len(code)] == code:
				result += key
				encode_str = encode_str[len(code):]
	return result

###################################################################
SAMPLE_NO = "1"
if __name__ == '__main__':
	prob_lst, string = list(lines.strip('\n') for lines in open("test" + SAMPLE_NO + ".txt"))
	prob_lst = [float(prob) for prob in prob_lst.split()]
	print(huffman_decode(prob_lst, string))