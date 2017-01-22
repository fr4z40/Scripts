#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Eduardo Frazão ( https://github.com/fr4z40 )
#
#   Licensed under the MIT License;
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#

from subprocess import call
from os import walk
from argparse import ArgumentParser, RawTextHelpFormatter

desc = '''
#
# Args
#
# f - change permissions to allow writing if necessary
# u - truncate and remove file after overwriting
# v - show progress
# x - do not round file sizes up to the next full block;
#     this is the default for non-regular files
# z - add a final overwrite with zeros to hide shredding
#
# e.g:
#   ./shred_dir.py -a=vzu -n 2 /full/path_folder/
#   python shred_dir.py -a=vzu -n 2 /full/path_folder/
#
'''

parser = ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
parser.add_argument('folder', type=str)
parser.add_argument('-a', '--arguments', type=str)
parser.add_argument('-n', '--iterations', type=str)
args = parser.parse_args()


cmd = []

if args.arguments:
    cmd.append(args.arguments)

if args.iterations:
    cmd.append('n')
    cmd.append(' '+args.iterations)

if not args.iterations and not args.arguments:
    quit()


cmd = ('shred -'+''.join(cmd))

for dr in walk(args.folder):
    for fl in dr[2]:
        print(fl)
        pth = ('"%s/%s"' % (dr[0], fl)).replace('//','/')
        cm = (cmd +' '+ pth)
        call(cm, shell=True)
