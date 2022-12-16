import re
def parse_initial_arrangement(initial_arrangement_input: list):
    initial_arrangement_input.pop()
    initial_arrangement = [ [] for _ in range(9)]
    while len(initial_arrangement_input) > 0:
        line = initial_arrangement_input.pop()
        j = 0
        for i in range(1, len(line), 4):
            if line[i] != ' ':
                initial_arrangement[j].append(line[i])
            j += 1
    return initial_arrangement

infile = open("input.txt", "r")

initial_arrangement_input = []
line = infile.readline()
while line.strip() != '':
    initial_arrangement_input.append(line)
    line = infile.readline()

initial_arrangement = parse_initial_arrangement(initial_arrangement_input)


for line in infile:
    line = line.strip()
    match = re.search("move (\d+) from (\d+) to (\d+)", line)
    times = int(match.group(1))
    source = int(match.group(2)) - 1
    dest = int(match.group(3)) - 1
    while times > 0:
        item = initial_arrangement[source].pop()
        initial_arrangement[dest].append(item)
        times -= 1

for l in initial_arrangement:
    print(l[len(l) - 1], end='')
print()