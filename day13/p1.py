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

with open('input.txt', 'r') as file:
    in_order = 0
    i = 1
    moreLines = True
    while moreLines:
        line1 = file.readline().strip()
        line2 = file.readline().strip()
        if line1 and line2:
            in_order += i * (compare_lines(eval(line1), eval(line2)) != 1)
        else:
            moreLines = False
        i += 1
        file.readline() # skip a line

print(in_order)
