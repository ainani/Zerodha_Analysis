# Volume Reversal Strategy
# 1st condition :
# 5 day's absolute price change > 100 days Standard deviation of price change
# 2nd condition:
# 5DayAvgVol (Average volume traded between last 1 to 5 days) < Past_5DayAvgVol (Average volume traded between last 5 to 10 days)
# Buy condition = Cond1 + Cond2 + Cond3: 5 day's absolute price change < 0
# Sell condition = Cond1 + Cond2 + Cond3: 5 day's absolute price change > 0
# Exit condition = End of 5th Day or Counter Signal

import time

start_time = time.clock()

import datetime
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nsepy import get_history


# pip install lxml

def find_no_of_working_days(start_date, end_date):
    daydiff = end_date.weekday() - start_date.weekday()
    days = ((end_date - start_date).days - daydiff) / 7 * 5 + min(daydiff, 5) - (max(end_date.weekday() - 4, 0) % 5)
    return days


no_of_work_day = 365
no_of_calender_day = no_of_work_day / 5 * 7
end_date = datetime.datetime.now() - datetime.timedelta(days=1)
start_date = end_date - datetime.timedelta(days=no_of_calender_day)

# making sure of getting n working day(ignore sat & sun)
days = int(find_no_of_working_days(start_date, end_date))
while days < no_of_work_day:
    no_of_calender_day = no_of_calender_day + (no_of_work_day - days)
    start_date = end_date - datetime.timedelta(days=no_of_calender_day)
    days = int(find_no_of_working_days(start_date, end_date))

row_num = 0
with open('NSEEquitySymbols.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)  # skip header
    for rowcsv in readCSV:
        stock_symbol = rowcsv[0]
        stock_name = rowcsv[1]
        row_num = row_num + 1
        data = get_history(symbol=stock_symbol, start=start_date, end=end_date)

        if data.empty:
            continue
        else:
            no_of_day = 0
            while (len(data) < no_of_work_day):  # making sure n day data is there
                no_of_day = no_of_day + 1
                data = get_history(symbol=stock_symbol, start=start_date - datetime.timedelta(days=no_of_day),
                                   end=end_date)
        # print(data)

        data['Last 5 Day Avg. Vol'] = data['Volume'].shift(1).rolling(
            window=5).mean()  # Average volume traded in last 5 days
        data['Previous-Last 5 Day Avg. Vol'] = data['Last 5 Day Avg. Vol'].shift(
            5)  # Average volume traded between last 5 to 10 days
        data['5 Day Price Change(5Day)'] = data['Close'].shift(1) - data['Close'].shift(
            5)  # Price change for the last 5 days
        pricechange_100day_roll = data.rolling(window=100)
        data['STD of 100 Day Price Change(5Day)'] = pricechange_100day_roll[
            '5 Day Price Change(5Day)'].std()  # Standard deviation of price change

        data.loc[:, 'signal'] = 0
        data.loc[:, 'c_signal'] = 0
        data.loc[:, 'exit'] = 0

        # Buy Signal and Sell Signal. Signal will be updated 1 if there is Buy signal and -1 if there is Sell Signal

        data.loc[((data['5 Day Price Change(5Day)'].abs() > data['STD of 100 Day Price Change(5Day)']) & (
                    data['Last 5 Day Avg. Vol'] < data['Previous-Last 5 Day Avg. Vol']) & (
                              data['5 Day Price Change(5Day)'] < 0)), 'signal'] = 1
        data.loc[((data['5 Day Price Change(5Day)'].abs() > data['STD of 100 Day Price Change(5Day)']) & (
                    data['Last 5 Day Avg. Vol'] < data['Previous-Last 5 Day Avg. Vol']) & (
                              data['5 Day Price Change(5Day)'] > 0)), 'signal'] = -1

        # In this block of code, we will implement the core of the strategy. Here we will check for the last entry signal, if the signal is more than 5 days old then we exit the position, else we will continue to hold it until the signal is 5 days old or a counter signal is generated.
        # Let us understand what we do in each of the if statements below:
        # First, we check if a new signal is generated, if it is then we will assign the c_signal column equal to the new signal, and then we update the exit criterion according to the signal generated. In this case, we will check if the signal is 1 if it is so, then we will mark the exit count as 1 otherwise, we will mark it as -1.
        # Next, we will check if the entry signal is same as the existing position. If it is so, then we will update the exit criterion depending on the position. For example, if you are already long then your c_signal would be 1, hence it will be incremented by 1. If you are short then your c_signal is -1 and your exit will be reduced by 1.
        # After this, we will update the exit criterion for an already existing long trade. We check if the exit value of the c_signal is less 5 days old, if this is the case then we verify if the continuing signal is same as the previous days then we increment the exit by 1.
        # Just as in the above step, we will update the exit criterion for an already existing short trade.
        # Next, we will update the exit criterion to 0 on the fifth day after entering the trade. This is one of the conditions of the strategy and accordingly we will close all positions on their 5th day.

        for i in range(len(data)):

            if ((data.iloc[i]['signal'] != 0) & (data.iloc[i]['signal'] != data.iloc[i - 1]['c_signal'])):
                data.iloc[i, data.columns.get_loc('c_signal')] = data.iloc[i, data.columns.get_loc('signal')]
                if data['signal'][i] == 1:
                    data.iloc[i, data.columns.get_loc('exit')] = 1
                else:
                    data.iloc[i, data.columns.get_loc('exit')] = -1
            if ((data['signal'][i] != 0) & (data['signal'][i] == data['c_signal'][i - 1])):
                data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'][i - 1]
                # if data['c_signal'][i-1]==1:
                #       data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])+1
                # else:
                #    data.iloc[i,data.columns.get_loc('exit')]=int(data['exit'][i-1])-1
                if ((data['exit'][i - 1] < 5) & (data['exit'][i - 1] > -5)):
                    data.iloc[i, data.columns.get_loc('exit')] = data['exit'][i - 1] + data['signal'][i]
                else:
                    data.iloc[i, data.columns.get_loc('exit')] = 0 + data['signal'][i]
            if ((data['signal'][i] == 0) & (data['exit'][i - 1] < 5) & (data['exit'][i - 1] > 0)):
                data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'][i - 1]
                data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'][i - 1]) + 1
            if ((data['signal'][i] == 0) & (data['exit'][i - 1] > -5) & (data['exit'][i - 1] < 0)):
                data.iloc[i, data.columns.get_loc('c_signal')] = data['c_signal'][i - 1]
                data.iloc[i, data.columns.get_loc('exit')] = int(data['exit'][i - 1]) - 1
            if ((data['signal'][i] == 0) & ((data['exit'][i - 1] == 5) | (data['exit'][i - 1] == -5))):
                data.iloc[i, data.columns.get_loc('c_signal')] = 0
                data.iloc[i, data.columns.get_loc('exit')] = 0

        # Return calculations
        data['return'] = np.log(data['Close'] / data['Close'].shift(1))  # Stock Returns i.e. Market Returns
        data['str_return'] = data['return'] * data['c_signal']  # Strategy Returns
        data['cu_str_return'] = 0
        data['cu_mar_return'] = 0
        expanding_100day = data.expanding(min_periods=100)
        data['cu_mar_return'] = expanding_100day['return'].sum()  # Stock Returns of 100 days
        data['cu_str_return'] = expanding_100day['str_return'].sum()  # Strategy Returns of 100 days

        data.to_csv(stock_symbol + '.csv')

print("Sharpe Ratio of Strategy in " + stock_symbol + " is " + str(
    (data['cu_str_return'].iloc[-1] - data['cu_mar_return'].iloc[-1]) / data['cu_str_return'].std()))
print("No of Stocks analysed:" + str(row_num))
print("Time elapsed:" + str(int((time.clock() - start_time) * 1000)) + " mili-sec")

# plt.figure(figsize=(10,7))
# plt.plot(data['cu_str_return'][100:], color='g',label='Strategy Returns')
# plt.plot(data['cu_mar_return'][100:], color='r',label='Market Returns')
# plt.legend(loc='best')
# plt.show()