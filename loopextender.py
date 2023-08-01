#!/usr/bin/env python3

''' quick problem solving
    i'll explain later
'''

import argparse
import os
import random
import sys


# setup arguments parser
argsparser = argparse.ArgumentParser()
argsparser.add_argument('infile', help='input file path')
argsparser.add_argument('outfile', help='output file path')
argsparser.add_argument('-o', '--overwrite', action='store_true', help='do not ask for confirmation to overwrite if output file already exists')
argsparser.add_argument('-s', '--shuffle', action='store_true', help='shuffle the output order')


# parse arguments
args = argsparser.parse_args()
args.infile = os.path.realpath(args.infile)
args.outfile = os.path.realpath(args.outfile)


# make sure we have input to work with and stop if there is none
if not os.path.isfile(args.infile):
    print(f'! input file does not exist: {args.infile}')
    sys.exit(2)


# ask for confirmation to overwrite if output file already exists
if not args.overwrite:
    if os.path.exists(args.outfile):
        print(f'! output file exists: {args.outfile}')
        response = input('  overwrite? [Y/n]: ').lower().strip() or 'y'
        if response != 'y':
            sys.exit(0)


# read input file and write to output file
with \
open(args.infile, 'r') as infile, \
open(args.outfile, 'w') as outfile:
    inlist = infile.readlines()

    if args.shuffle:
        random.shuffle(inlist)

    for line in inlist:
        line = line.strip()
        if not line \
        or line.startswith('#'):
            continue
        try:
            repetitions, filepath = line.split(',', 1)
        except Exception as e:
            print(f'! skipping bad line: {line}')
            print(f'  error: {e}')
            continue
        else:
            for i in range(0, int(repetitions)):
                outfile.write(f'{filepath}\n')
