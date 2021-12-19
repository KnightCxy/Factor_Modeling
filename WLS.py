import pandas as pd
import numpy as np
import statsmodels.api as sm
# Reminder: The time span is 2015-2019
# the first task is to test the effectiveness of single factor.(significance and monotone)
# the next two fuctions are designed to test the significance of single factor
factor_data = pd.read_csv('EBITDTtoEV.csv')
market_cap_data = pd.read_csv('Market_Value.csv')
industries_returns = pd.read_csv('Sector_Return.csv')
stock_return = pd.read_csv('PCT_CHA_1M.csv')
def remove_dates(data):
    columns = []
    for i in data:
        if '20' in i:
            columns.append(i[:7])
        else:
            columns.append(i)
    data.columns = columns 
    return data
factor_data = remove_dates(factor_data)
market_cap_data = remove_dates(market_cap_data)
industries_returns = remove_dates(industries_returns)
stock_return = remove_dates(stock_return)
market_cap_data.columns = factor_data.columns
industries_returns.columns = market_cap_data.columns
stock_return.columns = market_cap_data.columns

def sector_matrix(factor_data, stock_return, certain_date_of_industries_returns):
    sector = pd.DataFrame(columns = [certain_date_of_industries_returns.name], index=factor_data.index)
    for x in range(505):
        ind = factor_data.loc[x][1]
        sector.loc[x] = certain_date_of_industries_returns.loc[ind]

    sector = sector.astype('float')
    sector_indicator = pd.get_dummies(factor_data['industry']).astype('float')
    
    newsec = pd.concat([sector, sector_indicator], axis=1)
    for i in newsec:
        if i is not certain_date_of_industries_returns.name:
            newsec[i] = newsec[i] * newsec[certain_date_of_industries_returns.name]
    return newsec.iloc[:,1:]

def factor_return_test(factor_data, market_cap_data, industries_returns, stock_return):
    for i in stock_return:
        if '20' in i:
        
            X = pd.DataFrame(factor_data[i])

            sector = sector_matrix(factor_data,stock_return,industries_returns[i]) #输入日期,1/74, 得到一个 505X11 的矩阵, 11个影响变量
            for j in sector:
                X = X.join(sector[j]) #加入11个影响变量
            X = sm.add_constant(X)
            Y = stock_return[i]
            wls_model = sm.WLS(Y,X, weights = list(market_cap_data[i].values) )# 市值作为权重加权回归
            results = wls_model.fit()      
            print(results.params[1], results.tvalues[1]) 
factor_return_test(factor_data, market_cap_data, industries_returns, stock_return)

