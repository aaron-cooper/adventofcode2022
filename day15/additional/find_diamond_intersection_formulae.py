import sys
from sympy import *
from itertools import product


# An equation with an absolute value like |x - a| = y - b (1) can be written
# as a list of equations like [x = a - b + y, x = a + b - y] (2) such that for
# every tuple (x, y) that satisfies (1), there's at least 1 equation in (2) that
# is also satsified.
# However, there are also some tuples which satisfy some equations in (2)
# without satisfying (1), but I'll handle that elsewhere in my p2
#
# Given an equation and a variable which should be isolated, unfold will break
# an equation into 2^N equations as described above, where N is the number of
# absolute value operations in the equation
#
# The equations will give isolated_variable in terms of the other variables in
# the equation
def unfold(equation, isolated_variable):
    variables = variables_in_abs(equation)
    variables.append(isolated_variable)
    return unfold_recr(equation, variables, len(variables) - 1)


def unfold_recr(equation, variables, i):
    if len(variables) == 1:
        return [Eq(variables[0], solve(equation, variables[0]))]
    else:
        variable = variables[i]
        equations = []
        for function in solve(equation, variable):
            if isinstance(function, Piecewise):
                for expr, _ in function.args:
                    if expr == nan:
                        continue
                    equations.extend(unfold_recr(Eq(variable, expr), variables, i - 1))
            else:
                equations.append(Eq(variable, function))
        return equations

def variables_in_abs(expression):
    variables = []
    for arg in expression.args:
        if isinstance(arg, Abs):
            variables.extend(any_variables(arg))
        else:
            variables.extend(variables_in_abs(arg))
    return variables

def any_variables(expression):
    if isinstance(expression, Symbol):
        return [expression]
    else:
        variables = []
        for arg in expression.args:
            variables.extend(any_variables(arg))
        return variables

x, y, a, b, c, d, r, u = symbols("x, y, a, b, c, d, r, u", real=True)

# The equation for a diamond looks something like:
#   |x - a| + |y - b| = r
# where (a, b) is the centre of the diamond and r is the manhatten distance from
# any point on the diamond's edge to its centre.
#
# If we take the four line segments that form the edges of the diamond and
# convert each of them to line, then we'd get the four lines represented by
# these equations:
#   y = -a + b + r + x
#   y = a + b - r - x
#   y = -a + b - r + x
#   y = a + b + r - x
# The next 2 lines break down two diamonds into the equations described above

d1 = unfold(Eq(Abs(x-a) + Abs(y-b), r), x)
d2 = unfold(Eq(Abs(x-c) + Abs(y-d), u), x)

# for each line in d1, find its intersect with every line in d2
solutions = map(lambda t: solve(t, [x, y]), product(d1, d2))
# lines in d1 with the same slope as lines in d2 won't have intersections,
# filter them
solutions = filter(lambda s: bool(s), solutions)
# change from dictionaries to points, factor while we're at it
solutions = map(lambda t: (t[x].factor(), t[y].factor()), solutions)
solutions = map(lambda t: str(t), solutions)

print('\n'.join(solutions))