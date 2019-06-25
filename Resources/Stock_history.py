import numpy as np
import panda as pd
from nsepy import get_history
from datetime import date

y=2019
for i in range(5):
    sbin = get_history(symbol='FSL',
                   start=date(y,5,1),
                   end=date(y,5,2))
    print sbin[['Open', 'High', 'Low', 'Close', 'Last']]
    y=y-1
