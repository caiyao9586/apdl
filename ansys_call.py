#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import datetime
import os


def error_find(content):
    with open(content, 'r') as f:
        for line in f:
            if 'NUMBER OF ERROR' in line:
                error_num = int(line.split()[-1])
                return error_num


def ansys_call(ansys_path, work_dir, filename):

    time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    input_file = os.path.join(work_dir,
                              filename+'.inp')
    output_file = os.path.join(work_dir,
                               'output'+time+'.out')

    job_name = 'seal'
    path_string = ('"{}"  -p ane3fl -dir "{}" -j "{}" -s read -l en-us '
                   '-b -i "{}" -o "{}"').format(
        ansys_path, work_dir, job_name, input_file, output_file
    )

    subprocess.call(path_string)
    ansys_create_cdb = True
    if error_find(output_file):
        ansys_create_cdb = False
    return ansys_create_cdb


def main():
    ansys_path = r'C:\Program Files\ANSYS Inc\v160\ANSYS\bin\winx64\ansys160.exe'
    work_dir = r'D:\Python\Circle_Seal\ansys_workdir'
    filename = 'model'
    result = ansys_call(ansys_path, work_dir, filename)
    return result


if __name__ == '__main__':
    main()
