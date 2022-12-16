
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

def is_visible(grid, tree):
    tree_row, tree_col = tree

    tree_height = grid[tree_row][tree_col]

    visible_top = True
    visible_bottom = True
    visible_left = True
    visible_right = True

    for i in range(tree_row -1, -1, -1):
        if grid[i][tree_col] >= tree_height:
            visible_top = False
            break
    for i in range(tree_row + 1, rows):
        if grid[i][tree_col] >= tree_height:
            visible_bottom = False
            break
    for i in range(tree_col - 1, -1, -1):
        if grid[tree_row][i] >= tree_height:
            visible_left = False
            break
    for i in range(tree_col + 1, cols):
        if grid[tree_row][i] >= tree_height:
            visible_right = False
            break
    return visible_right or visible_left or visible_top or visible_bottom



visible = 0
for tree_pos in range_2d(range(rows), range(cols)):
    visible += int(is_visible(grid, tree_pos))

print (visible)