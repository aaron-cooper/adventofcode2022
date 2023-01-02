# I used Desmos to help finalize the formulae I used to calculate intersections
# between diamonds. This script parses the expressions from Desmos and turns
# them into python code. Classic case of spending 15 minutes automating what
# could have been done in 3 minutes

import re
import json
from sys import argv

formula_latex_pattern = re.compile(r"\(\\operatorname{(ceil|floor)}\(([abcdru\-+()]+)/2\),\\operatorname{(ceil|floor)}\(([abcdru\-+()]+)/2\)\)")

with open(argv[1], 'r') as f:
    expressions = json.load(f)

def parse_expression(exp):
    if m := formula_latex_pattern.match(exp):
        return m.groups()
    return None

expressions = list(map(lambda e: e['latex'], expressions))

expression_chars = {
    'a': 'x1', 
    'b': 'y1',
    'r': 'r1',
    'c': 'x2',
    'd': 'y2',
    'u': 'r2'
}

codes = []

i = 1
for expression in expressions:
    if not (match := parse_expression(expression)):
        continue
    
    xfn, xsum, yfn, ysum = match
    xsum = ''.join(map(lambda l: expression_chars[l] if l in expression_chars else l, xsum))
    ysum = ''.join(map(lambda l: expression_chars[l] if l in expression_chars else l, ysum))
    code = [
        f"class PointLocator{i}(PointLocator):",
        f"    def __call__(self, x1, y1, r1, x2, y2, r2):",
        f"        return (self.{xfn}_div({xsum}), self.{yfn}_div({ysum}))"
    ]
    code = '\n'.join(code)
    codes.append(code)
    i += 1

for code in codes:
    print()
    print(code)