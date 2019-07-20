import numpy as np
import pandas as pd
from nsepy import get_history
from datetime import date, timedelta

scrips = ['AMARAJABAT', 'DABUR', 'DMART', 'GODREJAGRO', 'HAVELLS', 'HEXAWARE', 'ITC', 'M&M', 'RBLBANK', 'RELIANCE',
          'TITAN', 'YESBANK']
avg = [651.31, 434.12, 1333.40, 497.16, 572.50, 324.50, 294.25, 665.69, 1073.18, 868.81, 141.24]
qty = [11, 20, 5, 8, 2, 2, 21, 12, 10, 5, 4, 54]

start_date = date.today() - timedelta(days=1)
end_date = date.today()


sym = []
close = []

for scrip in scrips:
    scrip_close = get_history(symbol=scrip,
                   start=start_date,
                   end=end_date)

    df = pd.DataFrame(scrip_close)
    sym.append(df[['Symbol']].to_csv(header=None, index=False).rstrip())
    close.append(df[['Close']].to_csv(header=None, index=False).rstrip())

print zip(sym, close, avg, qty)
#print sym
#print close
    #print df.shape[1]
    #print scrip, scrip_close['Close']

