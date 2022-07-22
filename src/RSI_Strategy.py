import logging
import pandas as pd
def RSI():
    stock_data = pd.read_csv('Reliance.csv')
    difference = stock_data['Close Price'].diff()
    up = difference.clip(lower=0)
    down = -1 * difference.clip(upper=0)
    ema_up = up.ewm(com=13, adjust =False).mean()
    ema_down = down.ewm(com=13, adjust =False).mean()
    relativeStrength = ema_up/ema_down
    rsi_data = 100 - (100 / (1 + relativeStrength))
    return rsi_data