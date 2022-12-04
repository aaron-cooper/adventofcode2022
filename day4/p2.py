import re

sum = 0
with open("input.txt", "r") as infile:
    for line in infile:
        m = re.search('(\d+)-(\d+),(\d+)-(\d+)', line)
        r1 = set(range(int(m.group(1)), int(m.group(2)) + 1))
        r2 = set(range(int(m.group(3)), int(m.group(4)) + 1))
        if len(r1.intersection(r2)) > 0:
            sum += 1

print (sum)
