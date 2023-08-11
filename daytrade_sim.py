import numpy as np
import analysis_stocks
import model
import os
import finance_data

def extract_unique_elements(input_array):
    unique_elements = set()
    for item in input_array:
        unique_elements.add(item[0])
        unique_elements.add(item[1])
    return list(unique_elements)
def subtract_elements(arr1, arr2):
    result = [item for item in arr2 if item not in arr1]
    return result
def get_today_index_df():
    return [[finance_data.get_stock_price_today("^NDX")[0], 0.0, finance_data.get_stock_price_today("^GSPC")[0], 0.0]]
def get_today_stock_price(stock_name):
    #Open
    return [[finance_data.get_stock_price_today(stock_name)[0]]]

def is_all_zero(dct):
    return all(value == 0 for value in dct.values())

target_portfolio_achieved = False

holding_stocks = {
    "long": {
        "qqq":0,
        "spy":0
    },
    "short": {}
}

file_path = "./dataset/hedge_stock_loss.csv"
if not os.path.exists(file_path):
    with open(file_path, "w") as file:
        file.write("stock,loss\n")
    print(f"{file_path} created with initial content.")
else:
    print(f"{file_path} already exists.")

# Main trading loop
while not target_portfolio_achieved:
    # Step 2: Buy SPY and QQQ Decision by creating loss info file
    model.run(get_today_index_df, get_today_stock_price, -1)

    # Step 3: Buy Hedge 'able' SPY/QQQ stocks strong correlated themselves
    upward_corr, downward_corr = analysis_stocks.analyze(0.87, 10, 10)
    short_stocks = extract_unique_elements(downward_corr)
    long_stocks = subtract_elements(extract_unique_elements(upward_corr), short_stocks)
    
    print("우상향 군집\t: ", long_stocks)
    print("헤지 포지션 군집\t: ", short_stocks)
    
    #계속 매입
    holding_stocks["long"]["qqq"] += 1
    holding_stocks["long"]["spy"] += 1
    
    # 우상향 기세가 더 강하면 SPY, QQQ 매수, 반대면 헷지 포지션 구축
    if(len(long_stocks) >= len(short_stocks)):
        holding_stocks["long"]["qqq"] += 1
        holding_stocks["long"]["spy"] += 1
    else:
        for stk in short_stocks:
            if stock in holding_stocks["long"]:
                holding_stocks["long"][stk] += 1
            else:
                holding_stocks["long"][stk] = 1

    # 사실 불가능한 코드. 다만 문맥상 집어넣음.
    # Step 4: Monitor and Repeat
    if is_all_zero(holding_stocks['long']) or is_all_zero(holding_stocks['short']):
        target_portfolio_achieved = True
        print("Target portfolio achieved. 현금 확보가 완료되어 트레이딩 프로그램을 종료합니다.")

    print("Monitoring portfolio and repeating...")

    #1회 반복 종료
    break
    #Timer ... 

print("Trading completed.")