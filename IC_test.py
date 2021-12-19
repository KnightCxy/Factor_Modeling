# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 13:08:01 2021

@author: zhang dejian
"""
import scipy
import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as stats

#print stats.stats.spearmanr(x,y)

def factor_IC_test(factor_data, market_cap_data, stock_return):
    """
    :param factor_data: the residual of the regression(factor exposure(t) with respect to market-cap(t) and
    industries factor(t)(dummy)
    :param stock_return: monthly stock return (t+1)
    :return: correlations between factor exposure(t) and stock return(t+1) (a dataframe)

    tips: We use this residual as a proxy of factor exposure, which is both industries-adjusted and market-cap-adjusted;
    Examine the mean (significance), std(stability), IR ratio(mean/std), the propotion that correlation>0 (direction)
    """
   
    Ic=pd.DataFrame()
    beta0=pd.DataFrame()
    length=min(factor_data.shape[1],market_cap_data.shape[1])#74
  
    for i in range(7,length):#2015-06
    
        y = np.array(factor_data.iloc[:,i]) # 因变量为factor第i数据
        x = np.array(market_cap_data.iloc[:,i]) # 自变量为第 i列数据
        x = sm.add_constant(x) # 若模型中有截距，必须有这一步
        model = sm.OLS(y, x).fit() # 构建最小二乘模型并拟合
        a=model.resid 
        beta0[i-7]=a
        
   # beta0=factor_data
    length=min(beta0.shape[1],stock_return.shape[1])
    for i in range(length):
        #Ic.append(scipy.stats.pearsonr(beta0.iloc[:,i], stock_return.iloc[:,i]))
        #Ic.append(stats.stats.spearmanr(beta0.iloc[:,i], stock_return.iloc[:,i]))
        Ic[i]=stats.stats.spearmanr(beta0.iloc[:,i], stock_return.iloc[:,i])
    residuals=Ic.iloc[0,:]
    p_value=Ic.iloc[1,:]
    
    print("%d residuals are:" % len(residuals))
     #print(Ic.iloc[0,:])  
    print("the %d p_value of the residuals are:" % len(residuals)) 
    # print(Ic.iloc[1,:])  
    
    print("the Percentage of positive residuals is:") 
    print(residuals[residuals>0].count()/len(residuals))
    print("the stand devition of the residual are: ")  
    print(residuals.std()) 
    print("the absulute mean of the residuals are: ")  
    residuals=residuals.abs()
    print(residuals.mean())
    
    print("the stand devition of the p_value are: ")  
    print(p_value.std()) 
    print("the absulute mean of the p_value are: ")  
    p_value=p_value.abs()
    print(p_value.mean())  
    
    
    return 0


if __name__ == '__main__':
    path0="C:/Users/zhang dejian/Downloads/resource/703/project/CI/Stock_return2.csv"
    path1="C:/Users/zhang dejian/Downloads/resource/703/project/CI/Market_Value.csv"
    
    path2="C:/Users/zhang dejian/Downloads/resource/703/project/CI/EP.csv"
    path3="C:/Users/zhang dejian/Downloads/resource/703/project/CI/BP.csv"
    path4="C:/Users/zhang dejian/Downloads/resource/703/project/CI/ROA.csv"
    path5="C:/Users/zhang dejian/Downloads/resource/703/project/CI/ROE.csv"
    path6="C:/Users/zhang dejian/Downloads/resource/703/project/CI/CFP.csv"
    path7="C:/Users/zhang dejian/Downloads/resource/703/project/CI/asset_to_liability.csv"
    path8="C:/Users/zhang dejian/Downloads/resource/703/project/CI/CF_to_Liability.csv"
    path9="C:/Users/zhang dejian/Downloads/resource/703/project/CI/debt_to_asset.csv"
    path10="C:/Users/zhang dejian/Downloads/resource/703/project/CI/RSI-30.csv"
    path11="C:/Users/zhang dejian/Downloads/resource/703/project/CI/Turnover.csv"
    path12="C:/Users/zhang dejian/Downloads/resource/703/project/CI/cash_ratio.csv"
    path13="C:/Users/zhang dejian/Downloads/resource/703/project/CI/Div_yeild.csv"
    path14="C:/Users/zhang dejian/Downloads/resource/703/project/CI/EBITDA_EV.csv"
    path15="C:/Users/zhang dejian/Downloads/resource/703/project/CI/volatility.csv"

    
    stock_return=pd.read_csv(path0)  
    market_cap_data=pd.read_csv(path1)  
    
    EP=pd.read_csv(path2)
    BP=pd.read_csv(path3)
    ROA=pd.read_csv(path4)
    ROE=pd.read_csv(path5)
    CFP=pd.read_csv(path6)
    asset_to_liability=pd.read_csv(path7)
    CF_to_Liability=pd.read_csv(path8)
    debt_to_asset=pd.read_csv(path9)
    RSI_30=pd.read_csv(path10)
    Turnover=pd.read_csv(path11)
    cash_ratio=pd.read_csv(path12)
    Div_yeild=pd.read_csv(path13)
    EBITDA_EV=pd.read_csv(path14)
    volatility=pd.read_csv(path15)
    # print(stock_return.head())
    # print(market_cap_data.head())
    # print(factor_data.head())
    
    print("**********the result of EP is:" )
    factor_IC_test(EP, market_cap_data,stock_return)
    print("**********the result of BP is:")
    factor_IC_test(BP, market_cap_data,stock_return)
    print("**********the result of ROA is:")
    factor_IC_test(ROA, market_cap_data,stock_return)
    print("**********the result of ROE is:")
    factor_IC_test(ROE, market_cap_data,stock_return)
    print("**********the result of CFP is:")
    factor_IC_test(CFP, market_cap_data,stock_return)
    print("**********the result of asset_to_liability is:")
    factor_IC_test(asset_to_liability, market_cap_data,stock_return)
    print("**********the result of CF_to_Liability is:")
    factor_IC_test(CF_to_Liability, market_cap_data,stock_return)
    print("**********the result of debt_to_asset is:")
    factor_IC_test(debt_to_asset, market_cap_data,stock_return)
    print("**********the result of RSI_30 is:")
    factor_IC_test(RSI_30, market_cap_data,stock_return)
    print("**********the result of Turnover is:")
    factor_IC_test(Turnover, market_cap_data,stock_return)
    
    print("**********the result of cash_ratio is:")
    factor_IC_test(cash_ratio, market_cap_data,stock_return)
    print("**********the result of Div_yeild is:")
    factor_IC_test(Div_yeild, market_cap_data,stock_return)
    print("**********the result of EBITDA_EV is:")
    factor_IC_test(EBITDA_EV, market_cap_data,stock_return)
    print("**********the result of volatility is:")
    factor_IC_test(volatility, market_cap_data,stock_return)

    # # 读取文本文件
    # data = pd.read_csv("./pvuv.txt", sep="\t")
    # data.to_excel("./output/pvuv_pandas.xls", index=False)
