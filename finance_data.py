import pandas as pd
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

def get_stock_price_scaled(history):
    scaler = MinMaxScaler()
    return scaler.fit_transform(history[["Open"]])
def get_stock_price_today(ticker):
    ticker = yf.Ticker(ticker)
    today = datetime.today().strftime('%Y-%m-%d')
    history = ticker.history(period="1mo")
    return get_stock_price_scaled(history)[0]

class CSVIndexReader:
    def __init__(self, index_files):
        self.index_files = index_files

    def read_and_merge(self):
        merged = pd.read_csv(self.index_files[0])
        for i in range(1, len(self.index_files)):
            df = pd.read_csv(self.index_files[i])
            merged = pd.merge(merged, df, on='Date', how='outer', suffixes=('', f'_{i}'))
        self.merged_index = merged
    def filter_data(self):
        #Date,Price,Change %,Price_1,Change %_1
        scaler = MinMaxScaler()
        self.merged_index = self.merged_index.drop(columns=["Open", "Open_1", "High", "High_1", "Low", "Low_1", "Vol.", "Vol._1"])
        for column in self.merged_index.columns:
            if column != "Date":
                self.merged_index[column] = self.merged_index[column].replace('[\$,%]', '', regex=True).astype("float32")
        self.merged_index['Price'] = scaler.fit_transform(self.merged_index[['Price']])
        self.merged_index['Price_1'] = scaler.fit_transform(self.merged_index[['Price_1']])

        return self.merged_index
