#!/usr/bin/env python3

import argparse
import os
import random
import sys


# setup arguments parser
argsparser = argparse.ArgumentParser()
argsparser.add_argument('infile', help='absolute or relative input file path')
argsparser.add_argument('outfile', help='absolute or relative output file path')
argsparser.add_argument('-c', '--check', action='store_true', help='check file paths from the input file for their existence')
argsparser.add_argument('-o', '--overwrite', action='store_true', help='do not ask for confirmation to overwrite if the output file already exists')
argsparser.add_argument('-s', '--shuffle', action='store_true', help='shuffle the output order')


# parse arguments
args = argsparser.parse_args()
args.infile = os.path.realpath(args.infile)
args.outfile = os.path.realpath(args.outfile)


# make sure we have input to work with and stop if there is none
if not os.path.isfile(args.infile):
    print(f'! input file path does not exist: {args.infile}')
    sys.exit(2)


# ask for confirmation to overwrite if output file already exists
if not args.overwrite:
    if os.path.exists(args.outfile):
        print(f'! output file path exists: {args.outfile}')
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
    outfile.write('#EXTM3U\n')
    for line in inlist:
        line = line.strip()
        if not line \
        or line.startswith('#'):
            continue
        try:
            repetitions, filepath = line.split(',', 1)
            if args.check:
                if not os.path.isfile(filepath):
                    raise Exception(f'file path does not exist')
        except Exception as e:
            print(f'! skipping line: {line}')
            print(f'  error: {e}')
            continue
        else:
            for i in range(0, int(repetitions)):
                outfile.write(f'{filepath}\n')
