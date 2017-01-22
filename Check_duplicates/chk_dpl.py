#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2017 Eduardo Frazão ( https://github.com/fr4z40 )
#
#   Licensed under the MIT License;
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#

from os import walk, stat
from sys import argv
from subprocess import check_output


if len(argv) != 2:
    print('how to use\n%s /full_path/folder/to_check/' % argv[0])
    quit()



def md5sum(file_path):
    rst = ((check_output(('md5sum "%s"' % file_path), shell=True)).decode())
    return(rst.split()[0].strip())



files = {}

for dr in walk(argv[1]):
    for fl in dr[2]:
        fl_path = (('%s/%s' % (dr[0], fl)).replace('//', '/')).strip()
        md5_rst = md5sum(fl_path)
        ctime = stat(fl_path).st_ctime
        if md5_rst not in files:
            files[md5_rst] = [[ctime, fl_path]]
        else:
            files[md5_rst].append([ctime, fl_path])


for key in files.keys():
    if len(files[key]) > 1:
        files[key] = sorted(files[key])
        files[key][0][1] = ('orig_file:'+(files[key][0][1].strip()))
        for item in files[key]:
            print(item[1])
