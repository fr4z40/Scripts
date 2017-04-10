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
from subprocess import check_output
from argparse import ArgumentParser, RawTextHelpFormatter



def md5sum(file_path):
    rst = ((check_output(('md5sum "%s"' % file_path), shell=True)).decode())
    return(rst.split()[0].strip())



if __name__ == '__main__':

    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('path', help='Folder Path', type=str)
    parser.add_argument('-d', '--detailed',
        help='0 or 1, if seted as 1, will be more verbose, default is 0', type=int)
    args = parser.parse_args()


    fd_pth = args.path
    files = {}

    for dr in walk(fd_pth):
        for fl in dr[2]:
            fl_path = (('%s/%s' % (dr[0], fl)).replace('//', '/')).strip()
            md5_rst = md5sum(fl_path)
            ctime = stat(fl_path).st_ctime
            if md5_rst not in files:
                files[md5_rst] = [[ctime, fl_path]]
            else:
                files[md5_rst].append([ctime, fl_path])


    if args.detailed == 1:
        out_p = []


    for key in files.keys():
        if args.detailed == 1:
            files[key] = sorted(files[key])
            for item in files[key]:
                ctm, pth = item[0], item[1]
                out_p.append((pth, ctm, key))
        else:
            if len(files[key]) > 1:
                files[key] = sorted(files[key])
                files[key][0][1] = ('orig_file:'+(files[key][0][1].strip()))
                for item in files[key]:
                    print(item[1])

    if args.detailed == 1:
        out_p = sorted(set(out_p))
        for item in out_p:
            print('%s|%s|%s' % (item[2], str(item[1]), item[0]))

