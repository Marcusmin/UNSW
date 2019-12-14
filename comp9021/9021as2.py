import re
from itertools import combinations
import math


def available_coloured_pieces(name):
    path = [each for each in list(name) if each != '\n'][1:-1]
    pattern = re.compile('"(.*)"')
    color = []
    all_coordinate = []
    for each in path:
        each = pattern.findall(each)
        temp = each[0].replace('" fill="', '')
        x = re.split(r'[LMz]',temp)
        color.append(x.pop())
        temp_no_null = [each for each in x if each != '']
        piece_temp = []
        for each in temp_no_null:
            temp_num = tuple([int(each) for each in each.split()])
            piece_temp.append(temp_num)
        all_coordinate.append(piece_temp)
    temp = zip(color, all_coordinate)
    dic = {c:a for c,a in temp}
    return dic

#part1

def cp(p1, p2, p3):
    num = (p2[0] - p1[0])*(p2[1] - p3[1]) - (p2[1] - p1[1])*(p2[0] - p3[0])
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1
def cp1(p1, p2, p3, p4):
    num = ((p2[0] - p1[0])*(p2[1] - p3[1]) - (p2[1] - p1[1])*(p2[0] - p3[0])) * ((p2[0] - p1[0])*(p2[1] - p4[1]) - (p2[1] - p1[1])*(p2[0] - p4[0]))
    if num > 0:
        return 1
    elif num == 0:
        return 0
    else:
        return -1
def test(all_coordinate):
    all_coordinate = all_coordinate.values()
    for each_piece in all_coordinate:
        if len(each_piece) < 3 or len(set(each_piece)) != len(each_piece):
            return False
        cp_sum = 0
        for i in range(len(each_piece)):
            cp_sum += cp(each_piece[(0+i) % len(each_piece)], each_piece[(1+i) % len(each_piece)], each_piece[(2+i) % len(each_piece)])
        if cp_sum == 1 * len(each_piece) or cp_sum == (-1) * len(each_piece):
            continue
        else:
            return False
    return True

#test(all_coordinate)

def test1(all_coordinate):
    all_coordinate = all_coordinate.values()
    for each_piece in all_coordinate:
        if len(each_piece) < 3:
            return False
        elif len(each_piece) == 3:
            return True
        cp_pro = 1
        for i in range(len(each_piece)):
            cp_pro *= cp1(each_piece[(0+i) % len(each_piece)], each_piece[(1+i) % len(each_piece)], each_piece[(2+i) % len(each_piece)], each_piece[(3+i) % len(each_piece)])
        if cp_pro >= 0:
            continue
        else:
            return False
    return True

#test1(all_coordinate)

def test2(all_coordinate):
    all_coordinate = all_coordinate.values()
    for each_piece in all_coordinate:
        temp = combinations(each_piece, 3)
        cp_0 = 1
        for each in temp:
            cp_0 *= cp(each[0], each[1], each[2])
        if cp_0 == 0:
            return False
    return True

def are_valid(all_coordinate):
    return test(all_coordinate) and test1(all_coordinate) and test2(all_coordinate)

#part2
def are_identical_sets_of_coloured_pieces(c1, c2):
    if len(c1) != len(c2) or set(c1.keys()) != set(c2.keys()) :
        return False
    c1_color = c1.keys()
    for each in c1_color:
        if same(c1[each], c2[each]):
            continue
        else:
            return False
    return True

def same(c1, c2):
    c1.append(c1[0])
    c2.append(c2[0])
    c1_side = set()
    c2_side = set()
    c1_angle = set()
    c2_angle = set()
    if len(c1) != len(c2):
        return False
    else:
        for i in range(len(c1)-1):
            c1_side.add(math.sqrt((c1[i][0] - c1[i+1][0])**2 + (c1[i][1] - c1[i+1][1])**2))
            c2_side.add(math.sqrt((c2[i][0] - c2[i+1][0])**2 + (c2[i][1] - c2[i+1][1])**2))
        c1.pop()
        c2.pop()
        for each in c1:
            i = c1.index(each)
            if i == len(c1)-1:
                    c1.append(c1[0])
                    c2.append(c2[0])
                    c1_angle.add(((c1[i-1][0]-c1[i][0])*(c1[i+1][0]-c1[i][0])+(c1[i-1][1]-c1[i][1])*(c1[i+1][1]-c1[i][1]))/(math.sqrt((c1[i-1][0]-c1[i][0])**2+(c1[i-1][1]-c1[i][1])**2)) * math.sqrt((c1[i+1][0]-c1[i][0])**2+(c1[i+1][1]-c1[i][1])**2))
                    c2_angle.add(((c2[i-1][0]-c2[i][0])*(c2[i+1][0]-c2[i][0])+(c2[i-1][1]-c2[i][1])*(c2[i+1][1]-c2[i][1]))/(math.sqrt((c2[i-1][0]-c2[i][0])**2+(c2[i-1][1]-c2[i][1])**2)) * math.sqrt((c2[i+1][0]-c2[i][0])**2+(c2[i+1][1]-c2[i][1])**2))
                    break
            c1_angle.add(((c1[i-1][0]-c1[i][0])*(c1[i+1][0]-c1[i][0])+(c1[i-1][1]-c1[i][1])*(c1[i+1][1]-c1[i][1]))/(math.sqrt((c1[i-1][0]-c1[i][0])**2+(c1[i-1][1]-c1[i][1])**2)) * math.sqrt((c1[i+1][0]-c1[i][0])**2+(c1[i+1][1]-c1[i][1])**2))
            c2_angle.add(((c2[i-1][0]-c2[i][0])*(c2[i+1][0]-c2[i][0])+(c2[i-1][1]-c2[i][1])*(c2[i+1][1]-c2[i][1]))/(math.sqrt((c2[i-1][0]-c2[i][0])**2+(c2[i-1][1]-c2[i][1])**2)) * math.sqrt((c2[i+1][0]-c2[i][0])**2+(c2[i+1][1]-c2[i][1])**2))
    if c1_side == c2_side and c1_angle & c2_angle:
        return True

#part3
def get_k(c1, c2):
    if c1[0] == c2[0]:
        return -1
    return (c1[1]-c2[1])/(c1[0]-c2[0])
def get_d(c1, c2):
    if c1[0] == c2[0]:
        return (abs(c1[0]))
    elif c1[1] == c2[1]:
        return (abs(c1[1]))
    return abs(c2[0]*c1[1]-c1[0]*c2[1])/(math.sqrt((c1[1]-c2[1])**2 + (c1[0]-c2[0])**2))
def get_l(c1, c2):
    if c1[0] == c2[0]:
        return (abs(c1[1]-c2[1]))
    elif c1[1] == c2[1]:
        return (abs(c1[0]-c2[0]))
    return math.sqrt((c1[0]-c2[0])**2+ (c1[0]-c2[0])**2)
def p_o_l(p,l):
    x1 = l[0][0]
    y1 = l[0][1]
    x2 = l[1][0]
    y2 = l[1][1]
    if x1 == x2:
        if y2 > y1:
            return p[0] == x1 and (y1<=p[1]<=y2)
        if y1 > y2:
            return p[0] == x1 and (y2<=p[1]<=y1)
    if y1 == y2:
        if x2 > x1:
            return p[1] == y1 and (x1<=p[0]<=x2)
        if x1 > x2:
            return p[1] == y1 and (x2<=p[0]<=x1)
    else:
        v1 = x1*(y2-y1)/(x2-x1) - (x1*y2-x2*y1)/(x2-x1)
        v2 = x2*(y2-y1)/(x2-x1) - (x1*y2-x2*y1)/(x2-x1)
        return p[1] == (p[0]*(y2-y1)/(x2-x1) - (x1*y2-x2*y1)/(x2-x1)) and ((x1<=p[0]<=x2) or (x2<=p[0]<=x1)) and ((v1<=p[1]<=v2) or (v2<=p[1]<=v1))
def is_solution(c1, c2):
    side_sum = {}
    line = []
    useless_line = []
    useful_line = []
    values  = list(c1.values())
    for each in values:
        each.append(each[0])
        for i in range(len(each)-1):
            line.append([each[i], each[i+1]])
    for each_line in line:
        for p in line:
            if p_o_l(p[0], each_line) and p_o_l(p[1], each_line):
                useless_line.append(p)
                useless_line.append(each_line)
    useless_line = [each for each in useless_line if useless_line.count(each)>2]
    for each in line:
        if each not in useless_line:
            useful_line.append(each)
    l1 = 0
    l2 = 0
    for each in useful_line:
        l = get_l(each[0], each[1])
        l1 += l
    c2_values = list(c2.values())[0]
    c2_values.append(c2_values[0])
    for i in range(len(c2_values)-1):
        l = get_l(c2_values[i], c2_values[i+1])
        l2 += l
    a1 = set()
    a2 =set()
    for each in useful_line:
        k = get_k(each[0], each[1])
        d = get_d(each[0], each[1])
        a1.add((k ,d))
    for i in range(len(c2_values)-1):
        k = get_k(c2_values[i], c2_values[i+1])
        d = get_d(c2_values[i], c2_values[i+1])
        a2.add((k, d))
    if l1 == l2 and a1 == a2:
        return True
    return False