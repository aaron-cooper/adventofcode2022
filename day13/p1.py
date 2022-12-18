def lex_line(line):
    lexed = []
    i = 0
    while i < len(line):
        if line[i] == '[':
            lexed.append('[')
            i += 1
        elif line[i] == ']':
            lexed.append(']')
            i += 1
        elif line[i] == ',':
            i += 1
        else: # digit
            j = i
            while line[j].isdigit():
                j += 1
            lexed.append(int(line[i:j]))
            i = j
    return lexed

with open('input.txt', 'r') as file:
    line = file.readline().strip()
    lexed = lex_line(line)
    for token in lexed:
        print(token)




