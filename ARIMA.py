import pandas as pd
import matplotlib.pyplot as plt
def estimate_factor_return(historical_factor_return):
    """
    :param historical_factor_return: a dataframe, containing all historical factors returns
    :return: the estimation of all factor return for next period

    tips: we have all historical factors returns from the above function. Then we use these historical factors returns
    to predict the future factor returns. There are many ways to do this, but here we just do something practical.
    we use ARMA (or ARIMA, test stationary first) and exponentially weighted moving average method(EWMA) respectively.
    So write two functions if necessary.
    """
    # Import data : Internet Usage per Minute
    df = pd.read_excel(historical_factor_return, index_col=0)
    print(df)

    # Original Series
    fig, axes = plt.subplots(3, 3)
    axes[0, 0].plot(df)
    axes[0, 0].set_title('Original Series')
    plot_acf(df, ax=axes[0, 1], lags=30)
    plot_pacf(df, ax=axes[0, 2], lags=30)

    # 1st Differencing
    axes[1, 0].plot(df.diff())
    axes[1, 0].set_title('1st Order Differencing')
    plot_acf(df.diff().dropna(), ax=axes[1, 1], lags=30)
    plot_pacf(df.diff().dropna(), ax=axes[1, 2], lags=30)

    # 2nd Differencing
    axes[2, 0].plot(df.diff().diff())
    axes[2, 0].set_title('2nd Order Differencing')
    plot_acf(df.diff().diff().dropna(), ax=axes[2, 1], lags=30)
    plot_pacf(df.diff().diff().dropna(), ax=axes[2, 2], lags=30)

    plt.show()

    # 1,3,3 ARIMA Model
    model = ARIMA(df, order=(1, 1, 1))
    model_fit = model.fit()
    print(model_fit.summary())

    # Plot residual errors
    residuals = pd.DataFrame(model_fit.resid)
    fig, ax = plt.subplots(1, 2)
    residuals.plot(title="Residuals", ax=ax[0])
    residuals.plot(kind='kde', title='Density', ax=ax[1])
    plt.show()

    # Actual vs Fitted
    # Forecast
    pred_vals = model_fit.predict()
    print(pred_vals)
    plt.plot(df)
    plt.plot(pred_vals)
    plt.legend(['original data', 'prediction'])
    plt.show()

    forecast = model_fit.forecast(5)
    print(forecast)