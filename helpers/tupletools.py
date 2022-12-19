from .sign import sign

def tuple_range(start, stop):
    for i in range(len(start)):
        if start[i] != stop[i]:
            break
    dir = sign(stop[i] - start[i])
    curr = list(start)
    while curr[i] != stop[i]:
        yield tuple(curr)
        curr[i] += dir
    yield tuple(curr)

def tuple_add(left, right):
    return tuple(map(sum, zip(left, right)))