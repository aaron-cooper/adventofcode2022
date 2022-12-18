from sortedcontainers import SortedList

class Index:
    def __init__(self, key, iterable):
        self.key = key
        self.under = {}
        self.under_sorted = SortedList()
        for i in iterable:
            self.add(i)

    def add(self, elem):
        k = self.key(elem)
        if k not in self.under:
            self.under[k] = set()
            self.under_sorted.add(k)
        self.under[k].add(elem)

    def remove(self, elem):
        k = self.key(elem)
        self.under[k].remove(elem)
        self.__clean(k)

    def peek_min(self):
        return self.__peek(0)

    def peek_max(self):
        return self.__peek(-1)

    def __peek(self, k_ind):
        k = self.under_sorted[k_ind]
        elem = self.under[k].pop()
        self.under[k].add(elem)
        return elem 

    def __clean(self, k):
        if not len(self.under[k]):
            self.under.pop(k)
            self.under_sorted.remove(k)


class MultiIndexSet:
    def __init__(self, iterable = None):
        self.under = set(iterable) if iterable else set()
        self.indicies = {}

    def add_index(self, key, index_id = None):
        index = Index(key, self.under)
        if not index_id:
            index_id = key
        self.indicies[index_id] = index

    def add(self, elem):
        self.__all_index(lambda i: i.add(elem))
        self.under.add(elem)

    def remove(self, elem):
        self.__all_index(lambda i: i.remove(elem))
        self.under.remove(elem)

    def pop_min(self, index):
        elem = self.indicies[index].peek_min()
        self.remove(elem)
        return elem

    def __len__(self):
        return len(self.under)

    def __contains__(self, elem):
        return elem in self.under

    def __all_index(self, f):
        for index in self.indicies.values():
            f(index)