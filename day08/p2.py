
class range_2d:
    def __init__(self, range1, range2):
        self.range1 = range1
        self.range2 = range2

    def __iter__(self):
        for i in self.range1:
            for j in self.range2:
                yield (i, j)


grid = []
with open("input.txt", "r") as infile:
    for line in infile:
        grid.append([int(c) for c in line.strip()])

rows = len(grid)
cols = len(grid[0])

def scenic_score(grid, tree):
    tree_row, tree_col = tree

    tree_height = grid[tree_row][tree_col]

    visible_top = tree_row
    for i in range(tree_row -1, -1, -1):
        if grid[i][tree_col] >= tree_height:
            visible_top = tree_row - i
            break

    visible_bottom = rows - tree_row - 1
    for i in range(tree_row + 1, rows):
        if grid[i][tree_col] >= tree_height:
            visible_bottom = i - tree_row
            break

    visible_left = tree_col
    for i in range(tree_col - 1, -1, -1):
        visible_left = tree_col - i
        if grid[tree_row][i] >= tree_height:
            break

    visible_right = cols - tree_col - 1
    for i in range(tree_col + 1, cols):
        visible_right = i - tree_col
        if grid[tree_row][i] >= tree_height:
            break

    return visible_top * visible_bottom * visible_left * visible_right



max_scenic_score = 0
for tree_pos in range_2d(range(rows), range(cols)):
    curr_scenic_score = scenic_score(grid, tree_pos)
    if max_scenic_score < curr_scenic_score:
        max_scenic_score = curr_scenic_score

print (max_scenic_score)