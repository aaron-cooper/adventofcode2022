from .sign import sign

def tuple_range(start, stop, step=None):
    tsize = len(start)
    if not step:
        step = []
        for i in range(tsize):
            step.append(sign(stop[i] - start[i]))
        if not any(step):
            yield start
            return
        step = tuple(step)
        direction = step
    else:
        direction = tuple(map(lambda i: sign(i), step))
    curr = start

    while all(map(lambda i: direction[i] == 0 or direction[i] == 1 and curr[i] <= stop[i] or direction[i] == -1 and curr[i] >= stop[i], range(tsize))):
        yield tuple(curr)
        curr = tuple_add(curr, step)


def tuple_add(left, right):
    return tuple(map(sum, zip(left, right)))