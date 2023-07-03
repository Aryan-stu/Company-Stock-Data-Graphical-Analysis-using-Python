import pandas as pd
import yfinance as yf
import datetime
import os
import matplotlib.pyplot as plt

data = pd.read_csv("EQUITY_L.csv")
ticker_symbol = ""
company_name = ""
while True:
    data_input = input("Enter the ticker symbol of the company: ")
    matching_rows = data[data["SYMBOL"] == data_input]
    if not matching_rows.empty:
        ticker_symbol = matching_rows["SYMBOL"].iloc[0]
        company_name = matching_rows["NAME OF COMPANY"].iloc[0]
        break
    else:
        print("Value not found. Please try again.")
print("You have entered ticker symbol of "+company_name)
ns='.NS'
ticker_symbol=ticker_symbol+ns

start_date = ""
while True:
    date_str = input("Enter starting date in yyyy-mm-dd format: ")
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        start_date = date.strftime("%Y-%m-%d")
        break
    except ValueError:
        print("Invalid date format. Please enter in yyyy-mm-dd format.")

end_date = ""
while True:
    date_str = input("Enter ending date in yyyy-mm-dd format: ")
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        end_date = date.strftime("%Y-%m-%d")
        break
    except ValueError:
        print("Invalid date format. Please enter in yyyy-mm-dd format.")

data = yf.download(ticker_symbol, start=start_date, end=end_date)
data['MA50'] = data['Close'].rolling(window=50).mean()
print(data.head())
if os.path.exists("stock-data.csv"):
    os.remove("stock_data.csv")
data.to_csv("stock_data.csv")

data = pd.read_csv("stock_data.csv")
data = data.replace("#", pd.NA)
missing_values = data.isnull().sum()
print("Missing Values:")
print(missing_values)
data = data.dropna()
if os.path.exists("cleaned_data.csv"):
    os.remove("cleaned_data.csv")
data.to_csv("cleaned_data.csv")

fig, axs = plt.subplots(1, 2)
data1 = pd.read_csv("cleaned_data.csv")
axs[0].plot(data1['Date'], data1['Low'], label='Low value')
axs[0].plot(data1['Date'], data1['High'], label='High value')
axs[0].set_xlabel('Date')
axs[0].set_ylabel('Value')
axs[0].set_title("Comparision of Low and high value between "+start_date+" and "+end_date)
axs[0].legend()

axs[1].plot(data1['Date'], data1['Open'], label='Open value')
axs[1].plot(data1['Date'], data1['Close'], label='Close value')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('Value')
axs[1].set_title("Comparision of Open and Close value between "+start_date+" and "+end_date)
axs[1].legend()

fig.suptitle(company_name)
plt.subplots_adjust(wspace=0.4)
plt.show()
