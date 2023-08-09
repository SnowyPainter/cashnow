import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
import os
import csv
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def data_filtering(input_file):
    data = pd.read_csv(input_file)
    data.dropna(inplace=True)
    data = data.drop(columns=["Open", "Low", "High", "Open_1", "Low_1", "High_1"])
    return data

def get_all_stock_df(limit=1):
    input_date_format = '%Y-%m-%d'
    output_date_format = '%m/%d/%Y'
    data_frames = []
    data_frame_names = []
    i = 0
    directory = './dataset/Stocks'
    for filename in os.listdir(directory):
        if i >= limit and limit > -1:
            break
        if filename.endswith('.txt'):
            print(f"reading {filename}")
            try:
                file_path = os.path.join(directory, filename)
                df = pd.read_csv(file_path)
                df = df[['Date', 'Open']]
                df['Date'] = pd.to_datetime(df['Date'], format=input_date_format).dt.strftime(output_date_format)
                df['Open'] = df['Open'].replace(',','').astype('float32')
                scaler = MinMaxScaler()
                df['Open'] = scaler.fit_transform(df[['Open']])
                data_frame_names.append(filename)
                data_frames.append(df)
            except pd.errors.EmptyDataError:
                print("The file is empty or has no columns to parse.")
            i+=1
    return data_frames, data_frame_names

def build_model():
    model = keras.Sequential([
        layers.Dense(units=32, activation="relu"),
        layers.Dense(units=32, activation="relu"),
        layers.Dense(1)
    ])
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])
    return model

input_file_path = './dataset/index_data.csv'
output_file_path = './dataset/hedge_stock_loss.csv'
epochs = 100
train_n = 2000

all_labels, names = get_all_stock_df(-1)

for labels, name in zip(all_labels, names):
    try:
        print(f"processing ... {name} dataframe")
        dataset = data_filtering(input_file_path)
        dataset = pd.merge(dataset, labels, on='Date', how='outer').dropna()
        scaler = MinMaxScaler()        
        dataset['Price'] = scaler.fit_transform(dataset[['Price']])
        dataset['Price_1'] = scaler.fit_transform(dataset[['Price_1']])
        #label = Open column
        x = dataset[dataset.columns.difference(['Date', 'Open'])]
        y = dataset['Open']
        model = build_model()
        history = model.fit(x, y, epochs=epochs, batch_size=512, verbose=0)
        fields=[name, np.mean(history.history['mse'])]
        with open(output_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
    except Exception as e:
       print(f"Training function error occurred while processing {name}, passed")