# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 20:15:22 2021

@author: chunl
"""

def find_factor_return(factor_data_1,factor_data_2,factor_data_3,factor_data_4,stock_return,sector_return):
    index_0 = sector_return.columns
    df0 = pd.DataFrame(index_0)
    index_1 = factor_data_1.columns
    df=pd.DataFrame(index_1)
    index_2= factor_data_2.columns
    df2 = pd.DataFrame(index_2)
    index_3 = factor_data_3.columns
    df3 = pd.DataFrame(index_3)
    index_4= stock_return.columns
    df4= pd.DataFrame(index_4)
    index_5 = factor_data_4.columns
    df5 = pd.DataFrame(index_5)
    params = pd.DataFrame(columns = np.arange(len(factor_data_1.columns)-2),index=[1,2,3,4,5])
    tvalues = pd.DataFrame(columns = np.arange(len(factor_data_1.columns)-2),index=[1,2,3,4,5])
    white_pvalues = pd.DataFrame(columns = np.arange(len(factor_data_1.columns)-2),index=[1])
    
    for i in range(65):
        new = pd.DataFrame(columns = [1,2,3,4,5],index=np.arange(505))
        Y = pd.DataFrame(columns = [1],index=factor_data_1.index)
        new[1] = factor_data_1[df.loc[i+8][0]]
        new[2] = factor_data_2[df2.loc[i+8][0]]
        new[3] = factor_data_3[df3.loc[i+8][0]]
        new[4] = factor_data_4[df5.loc[i+8][0]]
        for x in range(len(new[4])):
            new[5][x] = sector_return[df0.loc[i+8][0]][0]
        new=pd.DataFrame(new,dtype=np.float)
        Y[1] = stock_return[df4.loc[i+2][0]]
        new = add_constant(new,prepend=True)
        model_1 = sm.OLS(Y,new).fit()
        tvalues_temp = model_1.tvalues
        params_temp = model_1.params
        params[i]=params_temp
        tvalues[i] = tvalues_temp
        white_test = het_white(model_1.resid,model_1.model.exog)    
        white_pvalues[i][1] = white_test[1]
        
    return params,tvalues,white_pvalues

import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.stats.diagnostic import het_white
from statsmodels.api import add_constant

factor_data_1 = pd.read_csv('D:/BU/MF703/data/ROE.csv')
factor_data_2 = pd.read_csv('D:/BU/MF703/data/EBITDA_EV.csv')
factor_data_3 = pd.read_csv('D:/BU/MF703/data/profit_margin.csv')
factor_data_4 = pd.read_csv('D:/BU/MF703/data/volatility.csv')
stock_return = pd.read_csv('D:/BU/MF703/data/Stock_return.csv') 
sector_return = pd.read_csv('D:/BU/MF703/data/Sector_Return.csv')
#sector_return[df0.loc[3][0]][0]
params,tvalues,white_pvalues = find_factor_return(factor_data_1,factor_data_2,factor_data_3,factor_data_4,stock_return,sector_return)

params.to_excel("D:/BU/MF703/data/params.xlsx",'params')
tvalues.to_excel("D:/BU/MF703/data/tvalues.xlsx",'tvalues')
white_pvalues.to_excel("D:/BU/MF703/data/white_pvalues.xlsx",'white_pvalues')
