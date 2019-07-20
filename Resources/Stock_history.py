import numpy as np
import pandas as pd
from nsepy import get_history
from datetime import date, timedelta
import string

scrips = ['AMARAJABAT', 'DABUR', 'DMART', 'GODREJAGRO', 'HAVELLS', 'HEXAWARE', 'ITC', 'M&M', 'RBLBANK', 'RELIANCE',
          'TITAN', 'YESBANK']
avg = [651.31, 434.12, 1333.40, 497.16, 572.50, 324.50, 294.25, 665.69, 522.54, 1073.18, 868.81, 141.24]
qty = [11, 20, 5, 8, 2, 2, 21, 12, 10, 5, 4, 54]

start_date = date.today() - timedelta(days=1)
end_date = date.today()

sym = []
close = []
diff = []
cost = []

for scrip in scrips:
    scrip_close = get_history(symbol=scrip,
                              start=start_date,
                              end=end_date)

    df = pd.DataFrame(scrip_close)
    sym.append(df[['Symbol']].to_csv(header=None, index=False).rstrip())
    close.append(df[['Close']].to_csv(header=None, index=False).rstrip())

# print zip(close, avg)

for avg_item, close_item in zip(avg, close):
    diff.append(round(avg_item - float(close_item), 2))

for avg_item, qty_item in zip(avg, qty):
    cost.append(avg_item*qty_item)

records = zip(sym, close, avg, diff, qty)

print records

for rec in records:
    if rec[-2] > 0:
        print rec
        curr_cost = rec[2]*rec[4]
        new_qty = rec[4] + 1
        new_cost = curr_cost + float(rec[1])
        new_avg = new_cost / new_qty
        print "\t", new_avg
