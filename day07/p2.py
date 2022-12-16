class EntryType:
    DIRECTORY = 1
    FILE = 2

class DirectoryEntry:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.type = EntryType.DIRECTORY
        self.my_size = None

    def __iter__(self):
        return EntryIter(self)



    def add_child(self, child):
        self.children[child.name] = child

    def get_child(self, name):
        return self.children[name]

    def size(self):
        if self.my_size == None:
            sum = 0
            for e in self.children.values():
                sum += e.size()
            self.my_size = sum
        return self.my_size

class FileEntry:
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.my_size = size
        self.type = EntryType.FILE

    def size(self):
        return self.my_size

class EntryIter:
    def __init__(self, entry):
        self.entry = entry
        self.next = entry
        self.iter_stack = [iter(entry.children.values())]

    def __next__(self):
        if self.next == None:
            raise StopIteration
        ret = self.next
        exit = False
        while not exit:
            try:
                self.next = next(self.iter_stack[len(self.iter_stack) - 1])
                if self.next.type == EntryType.DIRECTORY:
                    self.iter_stack.append(iter(self.next.children.values()))
                exit = True
            except:
                if len(self.iter_stack) > 0:
                    self.iter_stack.pop()
                else:
                    self.next = None
                    exit = True
        return ret

root = curr_dir = DirectoryEntry('/')

with open("input.txt", "r") as infile:
    infile.readline()
    for line in infile:
        line = line.strip()
        splits = line.split(' ')
        if splits[0] == '$':
            if splits[1] == 'cd':
                if splits[2] == '..':
                    curr_dir = curr_dir.parent
                else:
                    curr_dir = curr_dir.get_child(splits[2])
        elif splits[0] == 'dir': # directory
            curr_dir.add_child(DirectoryEntry(splits[1], curr_dir))
        else: # file
            curr_dir.add_child(FileEntry(splits[1], curr_dir, int(splits[0])))

free_space = 70000000 - root.size()
need_to_free = 30000000 - free_space

min = 70000000 
for e in root:
    size = e.size()
    if size >= need_to_free:
        if min > size:
            min = size

print (min)