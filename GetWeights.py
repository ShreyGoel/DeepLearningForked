# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 19:37:15 2018

@author: Shrey
"""
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

text_file = r"train_package\9\backtestlog.txt"
with open(text_file, 'r') as myfile:
    data=myfile.read().replace('\n', '')
    
weights_text = re.findall(r"\[(.*?)\]", data)[2:]

weights = []
space = ""
nccy = 11

for x_iter in weights_text:
    x_iter = x_iter.split(" ")
    while space in x_iter:
        x_iter.remove("")
    if(len(x_iter) == nccy + 1):
        weights.append(x_iter)
    elif len(x_iter) == nccy:
        ccy = ['BTC']+[x.split("'")[1] for x in x_iter]

weights = pd.DataFrame(weights, columns=ccy).astype(np.float64)

weights_melt = weights[2392:].reset_index(drop=True)