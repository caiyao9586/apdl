import tkinter

import datetime
import os


kw = {
    'a': 1,
    'b': 2,
}


def a(x=1, **kwargs):

    return kwargs['a'], kwargs['b']


print(a(**kw))



