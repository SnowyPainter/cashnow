import pandas as pd
import os
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

#ascending = True : smallest
#ascending = False : largest
def get_top_n_rows(df, n, ascending):
    sorted_df = df.sort_values(by=df.columns[1], ascending=ascending)
    top_n_rows = sorted_df.head(n)
    return top_n_rows
def over_n_corr(matrix, n):
    high_correlation_pairs = []
    for column in matrix.columns:
        for index, value in matrix[column].items():
            if value > n and column != index:
                high_correlation_pairs.append((column, index, value))
    return high_correlation_pairs
def get_stock_data(datas):
    stock_datas = {}
    for index, row in datas.iterrows():
        file_name = row['stock']
        file_path = os.path.join('./dataset/Stocks', file_name)
        if os.path.exists(file_path):
            stock_data = pd.read_csv(file_path)
            scaler = MinMaxScaler()
            stock_data['Open'] = scaler.fit_transform(stock_data[['Open']])
            stock_datas[file_name.replace('.us.txt', '')] = stock_data['Open']
        else:
            print(f"File {file_name} not found.")
    return stock_datas

def analyze(corr_threshold=0.9, long_stocks=10, short_stocks=10):
    hedge_stock_loss_file = "./dataset/hedge_stock_loss.csv"

    df = pd.read_csv(hedge_stock_loss_file)

    low_n_rows = get_top_n_rows(df, long_stocks, True)
    top_n_rows = get_top_n_rows(df, short_stocks, False)

    long_df = pd.DataFrame(get_stock_data(low_n_rows)).dropna()
    hedge_df = pd.DataFrame(get_stock_data(top_n_rows)).dropna()

    long_corr_mat = long_df.corr()
    hedge_corr_mat = hedge_df.corr()
    '''
    print("SPY, QQQ와 같이 우상향하는 주식")
    print(over_n_corr(long_corr_mat, corr_threshold))
    print("지수와의 상관 관계가 약한 주식")
    print(over_n_corr(hedge_corr_mat, corr_threshold))
    '''
    return over_n_corr(long_corr_mat, corr_threshold), over_n_corr(hedge_corr_mat, corr_threshold) 