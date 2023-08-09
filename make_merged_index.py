import pandas as pd

file1 = "./dataset/nasdaq100.txt"
file2 = "./dataset/nikkei225.txt"
file3 = "./dataset/sse.txt"
file4 = "./dataset/s&p500.txt"

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)
def filter_csv(df):
    df = df.drop(columns=['Vol.'])
    for column in df.columns:
        if column != "Date":
            df[column] = df[column].replace('[\$,%]', '', regex=True).astype("float32")
    return df

dfs = [df1, df4]
dfs = list(map(filter_csv, dfs))

merged_data = dfs[0]
i = 1
for df in dfs[1:]:
    merged_data = pd.merge(merged_data, df, on='Date', how='outer', suffixes=('', f'_{i}'))
    i += 1

merged_file = "./dataset/index_data.csv"
merged_data.to_csv(merged_file, index=False)

print(f"데이터 프레임이 {merged_file}에 저장되었습니다.")