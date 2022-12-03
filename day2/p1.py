# A X = Rock, 1
# B Y = Paper, 2
# C Z = Scissors, 3

# loss = 0
# draw = 3
# win = 6

game_to_point = {
    "A X": 4,
    "A Y": 8,
    "A Z": 3,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 7,
    "C Y": 2,
    "C Z": 6
}
score = 0
with open("input.txt", "r") as infile:
    for line in infile:
        line = line.strip()
        score += game_to_point[line]

print(score)
