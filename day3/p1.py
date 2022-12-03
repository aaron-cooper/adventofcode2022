
def build_type_to_priority():
    type_to_priority = {}
    priority = 1
    for i in range(ord('a'), ord('z') + 1):
        type_to_priority[chr(i)] = priority
        priority += 1
    for i in range(ord('A'), ord('Z') + 1):
        type_to_priority[chr(i)] = priority
        priority += 1
    return type_to_priority

type_to_priority = build_type_to_priority()

def priority_of_common_item(l1, l2):
    s1 = set(l1)
    s2 = set(l2)
    intersect = s1.intersection(s2)
    if len(intersect) == 0:
        return 0
    return type_to_priority[intersect.pop()]


with open("input.txt", "r") as infile:
    sum = 0
    for line in infile:
        line = line.strip()
        sum += priority_of_common_item(line[0:len(line) // 2], line[len(line) // 2:])
    print (sum)
