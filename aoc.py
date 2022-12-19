# Script for running my AoC solutions. This lets me treat solutions as packages
# so that I can separate some code into different files if I feel it might be
# useful on other days.

import argparse
from importlib import import_module
from shutil import copy

parser = argparse.ArgumentParser(
    description="This is a parent script for running my AoC solutions. Specify a day and part."
)

parser.add_argument("day", type=int)
parser.add_argument("part", type=int)
parser.add_argument("subpart", type=str, nargs='?', default='')

args = parser.parse_args()

copy(f'day{str(args.day).zfill(2)}/input.txt', 'input.txt')

import_module(f"day{str(args.day).zfill(2)}.p{args.part}{args.subpart}")