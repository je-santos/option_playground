import yfinance as yf
import numpy as np


ticker = 'AAPL'
stock  = yf.Ticker(ticker)

opt_exp_dates = stock.options
opt_date_data = stock.option_chain( opt_exp_dates[0] ) #gets the info for the first option available

"""
The option DataFrame icludes the following data:
    
    -Last: The price of the last trade that went through.
    -change: how much the last price has changed since the previous close
    -bid: price at which buyers are trying to buy (ask is the opposite)
    -volume: how many contracts have been traded during the session. 
    -open interest: number of open positions in the contract that have not yet been offset.
"""

opt_calls = opt_date_data[0].copy(deep=True)
opt_puts  = opt_date_data[1].copy(deep=True)

def get_avg_bid_ask(df, percent_ask=0.5):   
    """
    percent ask is the weight to calculate the average 
    the default is 50/50
    """
    percent_bid=1-percent_ask
    # computes the weighted average of the bid and ask
    df.insert(4,'bid/ask',df['bid']*percent_bid + df['ask']*percent_ask)
    # computes the difference between strikes
    df.insert(3,'diff strikes', np.diff(df['strike'],prepend=0))
    # replaces the first value w/zero to avoid misleading diff strike
    df.loc[0,'diff strikes']=0
    # computes the difference between them
    df.insert(6,'diff b/a', np.diff(df['bid/ask'],prepend=0))
    return df

for financial in [opt_calls, opt_puts]: 
    try: 
        get_avg_bid_ask(financial)
    except: print('There is aready info in that df')
    
