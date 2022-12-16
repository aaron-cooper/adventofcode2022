
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

def priority_of_common_item(lists):
    if len(lists) == 0:
        return 0
    final_set = set(lists[0])
    for i in range(1, len(lists)):
        final_set = final_set.intersection(set(lists[i]))
    return type_to_priority[final_set.pop()]


with open("input.txt", "r") as infile:
    lines = [line.strip() for line in infile]
    sum = 0
    for i in range(0, len(lines), 3):
        sum += priority_of_common_item([lines[i], lines[i + 1], lines[i + 2]])
    print(sum)
