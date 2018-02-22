#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2018 Eduardo Frazão ( https://github.com/fr4z40 )
#
#   Licensed under the MIT License;
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     https://opensource.org/licenses/MIT
#

from os import walk, stat
from subprocess import check_output
from argparse import ArgumentParser, RawTextHelpFormatter

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
cpu_count = int(cpu_count())



def md5sum(file_path):
    try:
        rst = ((check_output(('md5sum "%s"' % file_path), shell=True)).decode())
        return(rst.split()[0].strip())
    except:
        return(None)



def do_chk(fl_pth):
    md5_rst = md5sum(fl_pth)
    if md5_rst != None:
        ctime = stat(fl_pth).st_ctime
    else:
        ctime = 0
        fl_pth = (bytes(fl_pth, 'utf-8', 'ignore')).decode()
    rst = {'ctime':ctime, 'path':fl_pth, 'md5':md5_rst}
    return(rst)






if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('path', help='Folder Path', type=str)

    parser.add_argument('-d', '--detailed',
        help='0 or 1, if seted as 1, will be more verbose, default is 0', type=int)

    parser.add_argument('-c', '--cores',
        help='number of cores to use, by default its "half".\n* Can be a number: 1...N\n\tscript.py -c 8 /full/path/folder/\n* Or text: half / full / single\n\tscript.py -c half /full/path/folder/', type=str)

    args = parser.parse_args()

    if args.cores:
        if args.cores.isnumeric():
            core_value = int(args.cores)
            if (core_value > cpu_count) or (core_value == 0):
                print("You can't set more cores than you have or set 0")
                quit()
        else:
            core_value = args.cores.lower()
            if core_value == "single":
                core_value = 1
            elif core_value == "half":
                core_value = int(cpu_count/2)
            elif core_value == "full":
                core_value = cpu_count
            else:
                quit()
    else:
        core_value = int(cpu_count/2)

    e = ProcessPoolExecutor(core_value)



    fd_pth = args.path
    files = {}

    paths = []
    for dr in walk(fd_pth):
        for fl in dr[2]:
            fl_path = (('%s/%s' % (dr[0], fl)).replace('//', '/')).strip()
            paths.append(fl_path)

    #######################################

    map_rst = (list(e.map(do_chk, paths)))
    for item_file in map_rst:
        if item_file['md5'] not in files:
            files[item_file['md5']] = [[item_file['ctime'], item_file['path']]]
        else:
            files[item_file['md5']].append([item_file['ctime'], item_file['path']])

    #######################################

    if args.detailed == 1:
        out_p = []

    for key in files.keys():
        if args.detailed == 1:
            files[key] = sorted(files[key])
            for item in files[key]:
                ctm, pth = item[0], item[1]
                out_p.append((pth, ctm, key))
        else:
            if ((len(files[key]) > 1) and (key != None)):
                files[key] = sorted(files[key])
                files[key][0][1] = ('orig_file:'+(files[key][0][1].strip()))
                for item in files[key]:
                    print(item[1])

    if args.detailed == 1:
        out_p = sorted(set(out_p))
        for item in out_p:
            print('%s|%s|%s' % (item[2], str(item[1]), item[0]))


