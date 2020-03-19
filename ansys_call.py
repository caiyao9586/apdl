#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
from inp_jou import main as apm, time_now


def error_find(content):
    """
    :param content: ansys output 文件
    :return: 建模过程中是否不正常退出，error数量
    """
    with open(content, 'r') as f:
        for line in f:
            if 'NUMBER OF ERROR' in line:
                error_num = int(line.split()[-1])
                return error_num


def ansys_call(ansys_path, work_dir, file_name):
    """
    :param ansys_path:
    :param work_dir:
    :param file_name:
    :return: 是否生成cdb文件True/False
    """
    time = time_now()
    input_file = os.path.join(work_dir,
                              file_name)
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
    file_name = apm()
    result = ansys_call(ansys_path, work_dir, file_name)
    return result


if __name__ == '__main__':
    main()
