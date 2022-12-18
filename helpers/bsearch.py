
# adapted from wikipedia
def bsearch(collection, elem, key=lambda x: x):
    l = 0
    r = len(collection)
    while l < r:
        m = (l + r) // 2
        if key(collection[m]) < key(elem):
            l = m + 1
        else:
            r = m
    return l if l < len(collection) and key(collection[l]) == key(elem) else ~l

