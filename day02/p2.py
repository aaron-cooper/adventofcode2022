# A = Rock, 1
# B = Paper, 2
# C = Scissors, 3

# X loss = 0
# Y draw = 3
# Z win = 6

game_to_point = {
    "A X": 3,
    "A Y": 4,
    "A Z": 8,
    "B X": 1,
    "B Y": 5,
    "B Z": 9,
    "C X": 2,
    "C Y": 6,
    "C Z": 7
}
score = 0
with open("input.txt", "r") as infile:
    for line in infile:
        line = line.strip()
        score += game_to_point[line]

print(score)
