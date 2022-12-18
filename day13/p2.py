from functools import cmp_to_key
from helpers.bsearch import bsearch

# sign is not mine
def sign(x):
  return int(x > 0) - int(x < 0)

def compare_lines(line1, line2):
    size = min(len(line1), len(line2))
    for i in range (size):
        if type(line1[i]) == type(line2[i]):
            if type(line1[i]) == list:
                if comparison := compare_lines(line1[i], line2[i]):
                    return comparison
            else: 
                if sign(line1[i] - line2[i]): # if they're not equal
                    return sign(line1[i] - line2[i])
        elif type(line1[i]) == list:
            if comparison := compare_lines(line1[i], [line2[i]]):
                return comparison
        else:
            if comparison := compare_lines([line1[i]], line2[i]):
                return comparison
    return sign(len(line1) - len(line2))

packets = []

with open('input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:
            packets.append(eval(line))

packets.sort(key=cmp_to_key(compare_lines))

div1ind = bsearch(packets, [[2]], key=cmp_to_key(compare_lines))
div1ind = div1ind if div1ind >= 0 else ~div1ind
div1ind += 1

div2ind = bsearch(packets, [[6]], key=cmp_to_key(compare_lines))
div2ind = div2ind if div2ind >= 0 else ~div2ind
div2ind += 2

print(div1ind * div2ind)