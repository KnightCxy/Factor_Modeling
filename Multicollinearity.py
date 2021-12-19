# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 16:14:36 2021

@author: 75638
"""
import pandas as pd 
def get_factor_returns_correlation(path1,path2):
    """
    we need to use this function to identify the potential multicollinearity in future regression
    :param factor_data: factors exposure (passing the single factor test)
    :return: first we get the correlation matrix between factors in one month, then testing next month, we will get a
    series of correlation matrix. Calculate the mean of absolute value of correlations for each pairs then generate this
    matrix, which is what we want.
    Remember: all factors being tested are in the same classification.
    """
    factor_data1=pd.read_csv(path1,index_col=0).iloc[:,1:]
    factor_data2=pd.read_csv(path2,index_col=0).iloc[:,1:]
    sum=0
    count=0
    for i in factor_data1.columns:
        data = pd.DataFrame()
        data[0]=factor_data1[i]
        data[1]=factor_data2[i]
        corr=data.corr()
        for i in range(corr.shape[0]):
            for j in range(corr.shape[1]):
                if j>i:
                    sum+=abs(corr.iloc[i][j])
                    count+=1
    mean=sum/count
    return mean
if __name__ == '__main__':
    path1="C:/Users/75638/OneDrive - UW/Desktop/data/ROE.csv"
    #path2="C:/Users/75638/OneDrive - UW/Desktop/data/CFP.csv"
    path2="C:/Users/75638/OneDrive - UW/Desktop/data/profit_margin.csv"
    #path2="C:/Users/75638/OneDrive - UW/Desktop/data/EBITDA_EV.csv"
    print('%.3f'%get_factor_returns_correlation(path1,path2))