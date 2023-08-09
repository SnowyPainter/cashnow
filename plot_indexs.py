import pandas as pd
import matplotlib.pyplot as plt

csv_file_path = './dataset/index_data.csv'
data = pd.read_csv(csv_file_path)

plt.figure(figsize=(10, 6))  # 그래프 크기 설정

plt.plot(data['Price'], label='NASDAQ100')
plt.plot(data['Price_1'], label='S&P500')

plt.title('Index Trends')
plt.xlabel('Trade Time')
plt.ylabel('Index Price')
plt.legend()
plt.grid(True)

plt.show()
