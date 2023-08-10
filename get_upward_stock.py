import pandas as pd
import os
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

def get_top_n_smallest_rows(df, n):
    sorted_df = df.sort_values(by=df.columns[1], ascending=True)
    top_n_rows = sorted_df.head(n)
    return top_n_rows

hedge_stock_loss_file = "./dataset/hedge_stock_loss.csv"

df = pd.read_csv(hedge_stock_loss_file)
long_stocks = 10
low_n_rows = get_top_n_smallest_rows(df, long_stocks)

stock_datas = {}

for index, row in low_n_rows.iterrows():
    file_name = row['stock']
    file_path = os.path.join('./dataset/Stocks', file_name)
    if os.path.exists(file_path):
        stock_data = pd.read_csv(file_path)
        scaler = MinMaxScaler()        
        stock_data['Open'] = scaler.fit_transform(stock_data[['Open']])
        stock_datas[file_name.replace('.us.txt', '')] = stock_data['Open']
    else:
        print(f"File {file_name} not found.")

df = pd.DataFrame(stock_datas).dropna()

correlation_matrix = df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title("Correlation Heatmap")
plt.show()