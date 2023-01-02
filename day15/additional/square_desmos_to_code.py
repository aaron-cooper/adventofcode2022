import json
import re
from itertools import *

varnames = {
    'x_{1}': 'sx1',
    'x_{2}': 'sx2',
    'y_{1}': 'sy1',
    'y_{2}': 'sy2',
    'a': 'dx',
    'b': 'dy',
    'r': 'dr'
}

with open('desmos_square_intersections.json', 'r') as f:
    expressions = json.load(f)

full = re.compile(r"(\(.*\))")
cramped_comma = re.compile(r',([\w+-])')
cramped_sign = re.compile(r"(\w)([+-])(\w)")

cleaned_expressions = []

for latex in map(lambda e: e["latex"], expressions):
    if not full.match(latex):
        continue

    while cramped_comma.search(latex):
        latex = cramped_comma.sub(r", \1", latex)

    while cramped_sign.search(latex):
        latex = cramped_sign.sub(r"\1 \2 \3", latex)
    for orig, new in varnames.items():
        latex = latex.replace(orig, new)

    cleaned_expressions.append(latex)

# def square_intersection1(sx1, sxy1, sx2, sy2, dx, dy, dr):
#     return (sx2, dx + dy + dr - sx2)

for i, expr in enumerate(cleaned_expressions):
    print(f"def square_intersection{i + 1}(sx1, sy1, sx2, sy2, dx, dy, dr):")
    print(f"    return {expr}")
    print()


i = 1

print('[')

for _ in range(4):
    print('    [')
    for _ in range(2):
        print(f'        [square_intersection{i}, square_intersection{i + 1}],')
        i += 2
    print('    ],')

print(']')