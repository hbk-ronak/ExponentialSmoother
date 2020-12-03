#####################################################
# AMS 691 Project 02
# A collection of functions for Exponential
# Smoothing
# By : Ronak Dilip Shah
# 
# the Documentation for this package can be
# found here
# https://hbk-ronak.github.io/ExponentialSmoother
#####################################################

import pandas as pd
import numpy as np

def format_time(data):
    """
        Given a dataFrame
        
        Parameters
        ----------
        data : pandas.core.frame.DataFrame
            DataFrame of the input trade data.
        
        Returns
        -------
        pandas.core.frame.DataFrame
            Dataframe with formatted timestamps.

    """
    data["Time"] = pd.to_datetime(data["Time"], format='%H%M%S%f')
    data = data.rename(columns={"Time":"Date_Time"})
    return data
    
def clean_data(datat, tradeType = None, timePeriod = None):
    """
        Given a dataFrame Filter out data based on
        time period, trade type or both.
        
        Parameters
        ----------
        data : pandas.core.frame.DataFrame
            DataFrame that needs to be cleaned.
        tradeType : None or list of strings
            list of trade types to be removed
            defaults to None doesn't remove any trade types
        volume : bool
            If true Outputs the cumulative Vol along with OHLV.
        Returns
        -------
        pandas.core.frame.DataFrame
            cleaned data frame.

    """
    data = format_time(datat)
    if tradeType:
        for tp in tradeType:
            data = data[~data['Sale Condition'].str.contains(tp)]
    if timePeriod:
        lower = timePeriod[0]
        upper = timePeriod[1]
        data = data[(data["Date_Time"] >= lower) & (data["Date_Time"] <= upper)]
    data = data.set_index("Date_Time")
    return data

def tick_resampler_aligned(data, dataPoints, volume = False):
    """
        Given a dataFrame, and tick size, resample into tick bars.
        
        Parameters
        ----------
        data : str
            DataFrame of the input trade data.
        dataPoints : int
            Size of the output after resampling i.e combine (data.shape[0]/dataPoints) ticks 
            together.
        volume : bool
            If true Outputs the cumulative Vol along with OHLV.
        Returns
        -------
        pandas.core.frame.DataFrame
            OHLCV data for given tick bar size.

    """
    # add this to remove outside trading hours
    #data = data[(data.index >= '1900-01-01 09:30:00.0') & (data.index <= '1900-01-01 16:30:00.0')]
    start = 0 
    ohlc = []
    size = int(np.floor(data.shape[0]/dataPoints))
    while(start<data.shape[0] and len(ohlc)<dataPoints-1):
        dftemp = data['Trade Price'][start:start+size].to_list()
        ohlc.append([dftemp[0], max(dftemp), min(dftemp), dftemp[-1], sum(data['Trade Volume'][start:start+size])])
        start = start+size
    
    dftemp = data['Trade Price'][start:].to_list()
    ohlc.append([dftemp[0], max(dftemp), min(dftemp), dftemp[-1], sum(data['Trade Volume'][start:])])
    
    OHLCV = pd.DataFrame(ohlc, columns=['Open', 'High', 'Low', 'Close', 'Vol'])

    if(volume==True):
        return OHLCV
    else: 
        return OHLCV[['Open', 'High', 'Low', 'Close']]


def create_db(listdb, symbol, Metric):
    """
        Creates a data structure that is fast and easy to manipulate
        
        Parameters
        ----------
        listdb : list
            list of data frames that needs to be combined.
        symbol : list
            list of tickers
        Metric : str
            Metric that needs to be extracted from the data frame
        Returns
        -------
        list
            [calendar, [tickers], np.array].
    """
    shape_ = [d.shape[0] for d in listdb]
    if shape_.count(shape_[0]) != len(shape_):
        print("data isn't aligned")
        return
    if len(listdb) != len(symbol):
        print("incorrect lengths")
        return
    else:
        res = []
        res.append(listdb[0].index)
        res.append(symbol)
        res.append(np.vstack((np.array(db[Metric]) for db in listdb)).T)
    return res

def get_log_return(df):
    """
        Get log returns for a time series
        
        Parameters
        ----------
        df : pandas.core.frame.DataFrame
            OHLCV Time series data
        
        Returns
        -------
        pandas.core.frame.DataFrame
            OHLCV with log returns computed as (1+(close - open)/close)
    """
    log_returns = pd.Series(np.log((df['Close'] - df['Open'])/df['Open'] + 1),name='log returns')
    return pd.concat([df,log_returns], axis=1)

def exponential_smoothing(data, lambda_ = 0.1, initialValue = None):
    """
        Smooths the time series using exponential smoothing
        for more details visit https://en.wikipedia.org/wiki/Exponential_smoothing
        
        Parameters
        ----------
        data : Array like object
            Time Series on which we want to apply exponential smoothing.
        lambda_ : float
            parameter for exponential smoothing
        initalValue : 
            s0 the starting point for exponential smoothing
            if None: s0 = data[0]
        Returns
        -------
        list
            smoothed Time Series
    """
    if initialValue:
        op = [initialValue]
    else:
        op = [data[0]]
    for i in range(1,len(data)+1):
        op.append(lambda_*data[i-1]+(1-lambda_)*op[i-1])
    return op[1:]
