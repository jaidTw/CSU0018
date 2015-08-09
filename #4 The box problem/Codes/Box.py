"""
CSU0018 Computer Algorithms
Programming Assignment 04
The Box Problem
"""
class box:
    def __init__(self, side_lst):
        side_lst.sort(reverse = True)
        self.side1, self.side2, self.side3 = side_lst
        self.vol = self.side1 * self.side2 * self.side3

    def can_contain(self, box):
        return self.side1 > box.side1 and self.side2 > box.side2 and self.side3 > box.side3

def main(boxes):
    boxes.sort(key = lambda box : box.vol)      # O(nlogn)
    adj_lst = {boxes[i] : [box for box in boxes[i:] if box.can_contain(boxes[i])] for i in range(len(boxes))}

    depth_table = {box : 1 for box in boxes}    # O(n^2)
    for box in boxes:
        for adj in adj_lst[box]:
            if depth_table[adj] < depth_table[box] + 1:
                depth_table[adj] = depth_table[box] + 1
    print(max(depth_table.values()))
#####################################################################################
SAMPLE_NO = 3
if __name__ == "__main__":
    main([box([int(line[0]), int(line[1]), int(line[2])]) for line in list(lines.strip('\n').split() for lines in open("test" + str(SAMPLE_NO) + ".in", 'r'))[1:]])