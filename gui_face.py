import tkinter

import datetime
import os


with open('a.txt', 'r') as f:
    for line in f:
        print(line, end='')
