"""
CSU0018 Computer Algorithms
Programming Assignment 02
LCS (continuous) - Dynamic Programming
"""
def main(str_a, str_b) :
	last = ""
	sub_dict = {}

	for a_idx in range(len(str_a)):
		for b_idx in range(len(str_b)):
			if str_a[a_idx] == str_b[b_idx]:
				if not a_idx in sub_dict:
					sub_dict[a_idx] = {b_idx}
				else:
					sub_dict[a_idx].add(b_idx)
	
	for sub_len in range(2, min(len(str_a), len(str_b))):
		pop_list = []
		for (a_idx, idx_set) in sub_dict.items():
			if a_idx + sub_len > len(str_a):
				pop_list.append(a_idx)
				continue
			remove_list = []
			for b_idx in idx_set:
				if b_idx + sub_len > len(str_b):
					remove_list.append(b_idx)
					continue
				a_tmp = str_a[a_idx:a_idx + sub_len]
				b_tmp = str_b[b_idx:b_idx + sub_len]
				if a_tmp != b_tmp:
					remove_list.append(b_idx)
				else:
					last = a_tmp
			for rm_idx in remove_list:
				idx_set.remove(rm_idx)
		for key in pop_list:
			sub_dict.pop(key)		
	print(last)

#################################################################################
SAMPLE_NO = "1"
if __name__ == '__main__':
	main(*list(lines.strip('\n') for lines in open("test" + SAMPLE_NO + ".txt"))[1:])