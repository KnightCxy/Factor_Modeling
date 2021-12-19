def construct_factor_stratified_portfolio(factor_data, stock_return, sector_weight):
    """
    add all required inputs or divide this function into several small ones if you want

    :param factor_data: after cleaning
    :return: stratified portfolios and weights for each stocks (each month) including S&P500

    tips: descending sort the factor data within industries, divide into 5 parts within industries, each stock has
    same weight in each part, keep industry-neutral with SP500 (which means the weight of each industry should be equal
    to the weight of this industry in SP500), the first-ranked portfolio(i.e. portfolio constructed by stocks with top20%
    factor exposure in their industry)

    Bonus: consider the long-short portfolio (long first_ranked and short last-ranked portfolio), do the same thing above
    (another function); further, consider market-cap-weighted-adjusted(not equal-weighted) portfolio
    """
    factor = pd.read_csv(factor_data, index_col=0)
    stock_return = pd.read_csv(stock_return,index_col=0)
    sector_weight = pd.read_excel(sector_weight, index_col=0)
    factor.groupby('industry')
    factor_time_columns = list(factor.columns)
    stock_time_columns = list(stock_return.columns)
    sector_time_columns = list(sector_weight.columns)
    stratified_portfolio_return = pd.DataFrame()
    quantile_interval = [0, 0.2, 0.4, 0.6, 0.8]
    for num in range(len(stock_time_columns)):
        portfolio_return = []
        for j in quantile_interval:
            label = []
            for i in range(1, 12):
                temp = factor[factor['industry'] == i]
                a = temp[factor_time_columns[num + 6]].quantile(j)
                b = temp[factor_time_columns[num + 6]].quantile(j + 0.2)
                temp2 = temp[(a <= temp[factor_time_columns[num + 6]]) & (temp[factor_time_columns[num + 6]] <= b)]
                label.append(list(temp2.index))
            one_period_stock_return = stock_return[stock_time_columns[num]]
            one_period_sector_weight = sector_weight[sector_time_columns[num + 6]]
            portfolio_return_temp = 0
            for i in range(1, 12):
                temp_return = 0
                for k in label[i - 1]:
                    temp_return += one_period_stock_return[k]
                portfolio_return_temp += (temp_return / len(label[i - 1])) * one_period_sector_weight[i - 1]
            portfolio_return.append(portfolio_return_temp)
        stratified_portfolio_return[stock_time_columns[num]] = portfolio_return
    stratified_portfolio_return.index = ['tier 5', 'tier 4', 'tier 3', 'tier 2', 'tier 1']
    stratified_portfolio_return = stratified_portfolio_return.T
    stratified_portfolio_return = stratified_portfolio_return + 1
    stratified_portfolio_return = stratified_portfolio_return.cumprod()
    # stratified_portfolio_return.index = pd.to_datetime(stratified_portfolio_return.index)
    print(stratified_portfolio_return)
    plt.plot(stratified_portfolio_return)
    plt.legend(stratified_portfolio_return.columns)
    plt.title('stratified portfolio cumulative return')
    plt.show()