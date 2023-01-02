# Script for running my AoC solutions. This lets me treat solutions as packages
# so that I can separate some code into different files if I feel it might be
# useful on other days.

import argparse
from shutil import copy

parser = argparse.ArgumentParser(
    description="This is a parent script for running my AoC solutions. Specify a day and part."
)

parser.add_argument("day", type=int)
parser.add_argument("part", type=int)
args = parser.parse_args()

exec(f"from day{str(args.day).zfill(2)} import tests{args.part}")
