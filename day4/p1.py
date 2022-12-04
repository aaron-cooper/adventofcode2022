import re

sum = 0
with open("input.txt", "r") as infile:
    for line in infile:
        m = re.search('(\d+)-(\d+),(\d+)-(\d+)', line)
        r1 = set(range(int(m.group(1)), int(m.group(2)) + 1))
        r2 = set(range(int(m.group(3)), int(m.group(4)) + 1))
        if r1.issubset(r2) or r2.issubset(r1):
            sum += 1

print (sum)
