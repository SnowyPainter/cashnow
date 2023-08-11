import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
import os
import csv
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
index_data_csv = './dataset/index_data.csv'
output_loss_file_csv = './dataset/hedge_stock_loss.csv'
epochs = 100

def data_filtering(input_file):
    data = pd.read_csv(input_file)
    data.dropna(inplace=True)
    data = data.drop(columns=["Open", "Low", "High", "Open_1", "Low_1", "High_1"])
    return data
def build_model():
    model = keras.Sequential([
        layers.Dense(units=32, activation="relu"),
        layers.Dense(units=32, activation="relu"),
        layers.Dense(1)
    ])
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])
    return model

def run(get_today_index_df, get_today_stock_price, limit=1):
    input_date_format = '%Y-%m-%d'
    output_date_format = '%m/%d/%Y'
    i = 0
    directory = './dataset/Stocks'

    x_test = get_today_index_df()

    for filename in os.listdir(directory):
        if i >= limit and limit > -1:
            break
        if filename.endswith('.txt'):
            stock_name = filename.replace('.us.txt', '')
            print(f"reading {stock_name} txt file")
            file_path = os.path.join(directory, filename)
            try:
                scaler = MinMaxScaler()

                stock_df = pd.read_csv(file_path)
                stock_df = stock_df[['Date', 'Open']]
                stock_df['Date'] = pd.to_datetime(stock_df['Date'], format=input_date_format).dt.strftime(output_date_format)
                stock_df['Open'] = stock_df['Open'].replace(',','').astype('float64')
                stock_df['Open'] = scaler.fit_transform(stock_df[['Open']])
                
                print(f"\tdeep-learning {stock_name}")
                dataset = data_filtering(index_data_csv)
                dataset = pd.merge(dataset, stock_df, on='Date', how='outer').dropna()     
                dataset['Price'] = scaler.fit_transform(dataset[['Price']])
                dataset['Price_1'] = scaler.fit_transform(dataset[['Price_1']])
                #label = Open column
                x = dataset[dataset.columns.difference(['Date', 'Open'])]
                y = dataset['Open']
                model = build_model()
                model.fit(x, y, epochs=epochs, batch_size=512, verbose=0)
                
                y_test = get_today_stock_price(stock_name)

                loss, _ = model.evaluate(x_test, y_test)
                fields = [filename, loss]
                print(f"\tevaluating {stock_name} : {loss}")
                with open(output_loss_file_csv, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
            except pd.errors.EmptyDataError:
                print("The file is empty or has no columns to parse.")
            except Exception as e:
                print(e)
            i+=1