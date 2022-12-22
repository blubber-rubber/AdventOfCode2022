import time

start_time = time.time()

with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]


class Directory:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.filesizes = 0
        self.directories = {}

    def add_file(self, size):
        self.filesizes += size

    def move_up(self):
        return self.parent

    def move_down(self, name):
        if not name in self.directories:
            self.directories[name] = Directory(name, self)
        return self.directories[name]


home = Directory('/', None)

current_dir = home

for line in lines:
    if line.startswith('$ cd '):
        line = line.split(' ')[2]
        if line == '..':
            current_dir = current_dir.move_up()
        elif line == '/':
            current_dir = home
        else:
            current_dir = current_dir.move_down(line)
    elif not line.startswith('$') and not line.startswith('dir'):
        size = int(line.split(' ')[0])
        current_dir.add_file(size)

THRESHOLD = 100000


def dfs(current_dir: Directory, result):
    filesize = current_dir.filesizes
    for dir in current_dir.directories.values():
        filesize += dfs(dir, result)
    if filesize <= THRESHOLD:
        result.append(filesize)
    return filesize

result=[]

dfs(home, result)
print(sum(result))
print(time.time() - start_time)
