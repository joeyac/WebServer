# -*- coding: utf-8 -*-
from __future__ import print_function
from oj.wsgi import *
from utils.get_oj_problem import import_hdu_problem


# import_hdu_problem(1099)
for i in range(1000,1100):
    import_hdu_problem(i)






Theme = (
    'cerulean',
    'cosmo',
    'cyborg',
    'darkly',
    'flatly',
    'journal',
    'lumen',
    'paper',
    'readable',
    'sandstone',
    'simplex',
    'slate',
    'Spacelab',
    'superhero',
    'united',
    'yeti',
)
base = '<li><a href="theme/{item_name1}">{item_name2}</a></li>'
for item in Theme:
    pass
    #       <li><a href="theme/{item_name1}">{item_name2}</a></li>
    # print(base.format(item_name1=item, item_name2=item.capitalize()))
