from os import getcwd, path, chdir, mkdir
from subprocess import run
from sys import argv
from fileinput import input
from shutil import copy

def update_debug_config(day, part):
    with input(files=('.vscode/launch.json'), inplace=True) as f:
        for line in f:
            if 'args' in line:
                line = f'            "args": ["{day}", "{part}"]\n'
            print(line, end='')

def touch(file):
    run(['touch', file])

def commit_curr_dir_contents(day, part):
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', f'add day {day} part {part}'])

def dayn(day):
    return f'day{str(day).zfill(2)}/'

def vscode(file):
    run(['code', file])


chdir(path.join(getcwd(), path.dirname(argv[0])))

i = 1
while path.exists(dayn(i)):
    i += 1

if not path.exists(dayn(i - 1) + 'p2.py'): # move from p1 to p2
    i -= 1
    commit_curr_dir_contents(i, 1)
    dir = dayn(i)
    copy(dir + 'p1.py', dir + 'p2.py')
    update_debug_config(i, 1)
    vscode(dir + 'p2.py')
else:
    commit_curr_dir_contents(i, 2)
    dir = dayn(i)
    mkdir(dir)
    touch(dir + '__init__.py')
    touch(dir + 'p1.py')
    touch(dir + 'input.txt')
    update_debug_config(i, 2)
    vscode(dir + 'p1.py')