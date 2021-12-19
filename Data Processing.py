# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 14:51:01 2021

@author: 75638
"""
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 10000)
def process_data(path1,path2):
    '''
    1.path1: file path of different factor
    2.path2:file path of SP500members
    3.remove anomalies
    4.normalized data
    5.fill NaN with 0
    '''
    #read factor.xlsx
    factor=pd.read_excel(path1,index_col=0) 
    #remove anomalies which is greater than median+5*std or less than median-s*std
    for date in factor:
        median=factor[date].quantile(0.5)
        std=factor[date].std()
        min=median-5*std
        max=median+5*std     
        factor[date]=factor[date].clip(min,max)
    #normalize data
    for date in factor:
        mean=factor[date].mean()
        std=factor[date].std()
        factor[date]=(factor[date]-mean)/std
    # fill NAN 
    for date in factor:
        median=factor[date].quantile(0.5)
        factor.fillna(median,inplace=True)
    #read SP500 member datas
    member=pd.read_excel(path2,index_col=0)
    #merge industry data
    factor=pd.merge(member,factor,left_index=True,right_index=True)
    # save processed data
    factor.to_csv('C:\\Users\\75638\\OneDrive - UW\\Desktop\\703project\\data\\volatility.csv')
    return factor
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
    order = 2
    for j in data:
        if '20' in j:
            year = j.split('/')[2]
            month = j.split('/')[0]
            month =(int)(month)
            time_1 = year  + '-' +str(month+1)
            time_2 = year  + '-' +str(month+2)
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

if __name__ == '__main__':
    path1='C:\\Users\\75638\\OneDrive - UW\\Desktop\\703project\\original_data\\volatility.xlsx'
    path2='C:\\Users\\75638\\OneDrive - UW\\Desktop\\703project\\SP500\\SP500members.xlsx'
    data=process_data(path1,path2)