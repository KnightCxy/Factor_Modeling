# -*- coding: utf-8 -*-

# -- Sheet --

import pandas as pd
import numpy as np

def remove_dates(data):
    columns = []
    for i in data:
        if '20' in i:
            columns.append(i[:7])
        else:
            columns.append(i)
    data.columns = columns 
    return data

def Seasonal_data_fill(path):
    data = pd.read_csv('{}'.format(path))
    columns = []
    for i in data:
        if '20' in i:
            columns.append(i[:7])
        else:
            columns.append(i)
    data.columns = columns 
    order = 2
    for j in data:
        if '20' in j:
            year = j[:4]
            month = int(j[5:])
            time_1 = year + '-' + str(month+1)
            time_2 = year + '-' + str(month+2)
            data.insert(order+1, '{}'.format(time_1), np.nan)
            data.insert(order+2, '{}'.format(time_2), np.nan)
            order += 3
    temp = data.iloc[:,:2]
    data = data.iloc[:,2:]
    data = data.ffill(axis = 1)
    data = pd.concat([temp, data], axis = 1)
    data.columns = remove_dates(pd.read_csv('PE.csv')).columns
    data = data.set_index(data.columns[0])    
    return data.to_csv('New {}'.format(path))


df = pd.read_csv('salesgrowthrate.csv')
df.columns = remove_dates(pd.read_csv('PE.csv')).columns
df = df.ffill(axis = 1)
df.to_csv('New salesgrowthrate.csv')

