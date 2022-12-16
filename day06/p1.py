pattern_length = 4

with open("input.txt", "r") as infile:
    input_stream = infile.readline()

char_to_occurances = {chr(c): 0 for c in range(97, 97 + 26)}
duplicates = 0

for i in range(pattern_length):
    char_to_occurances[input_stream[i]] += 1
    if char_to_occurances[input_stream[i]] > 1:
        duplicates += 1

for i in range(pattern_length, len(input_stream)):
    if char_to_occurances[input_stream[i - pattern_length]] > 1:
        duplicates -= 1
    char_to_occurances[input_stream[i - pattern_length]] -= 1
    char_to_occurances[input_stream[i]] += 1
    if char_to_occurances[input_stream[i]] > 1:
        duplicates += 1
    if (duplicates == 0):
        print(i + 1)
        break
