import pandas as pd
import yfinance as yf
import json
import pytz

from operator import itemgetter
from app.database import Database
from datetime import datetime

db = Database()

def calculate_rsi(close_prices):
    change = close_prices.diff()
    change.dropna(inplace=True)

    # Create two copies of the Closing price Series
    change_up = change.copy()
    change_down = change.copy()

    #
    change_up[change_up < 0] = 0
    change_down[change_down > 0] = 0

    # Verify that we did not make any mistakes
    change.equals(change_up + change_down)

    # Calculate the rolling average of average up and average down
    avg_up = change_up.rolling(14).mean()
    avg_down = change_down.rolling(14).mean().abs()

    rsi = 100 * avg_up / (avg_up + avg_down)

    return rsi.iloc[-1]


# def calculate_macd(price):
#     # Get the 26-day EMA of the closing price
#     k = price.ewm(span=12, adjust=False, min_periods=12).mean()
#     # Get the 12-day EMA of the closing price
#     d = price.ewm(span=26, adjust=False, min_periods=26).mean()

#     macd = pd.DataFrame(k - d).rename(columns={"Close": "macd"})
#     signal = pd.DataFrame(macd.ewm(span=9, adjust=False, min_periods=9).mean()).rename(
#         columns={"macd": "signal"}
#     )
#     hist = pd.DataFrame(macd["macd"] - signal["signal"]).rename(columns={0: "hist"})
#     frames = [macd, signal, hist]
#     df = pd.concat(frames, join="inner", axis=1)

#     return df

def calculate_change(today, prev):
    return (today - prev) / prev

def format_ma(close, ma):
    return "Over" if close >= ma else "Under"

def update_config(config):
    with open('./config/config.json', 'w', encoding='utf-8') as json_file:
        json.dump(config, json_file)

def fetch_data():
    data = []
    stocks_data = {}
    all_stocks = []
    eastern = pytz.timezone('US/Eastern')
    time = datetime.now(tz=eastern).strftime("%m/%d/%Y, %H:%M:%S")
    db.update("stats", {"last_update": time})

    for document in db.get_categories(): 
        category, stocks = itemgetter('category', 'stocks')(document)  
        all_stocks += stocks

        for stock in stocks:
            stocks_data[stock] = {"category": category}
    
    tickers = yf.Tickers(" ".join(all_stocks))    

    for stock in all_stocks:
        try:
            df = tickers.tickers[stock].history(interval="1d", period="1y")
            close_prices = df["Close"]
            volume = df["Volume"]
            mean_volume = round(volume.tail(45).mean())
            latest_volume = volume.iloc[-1]
        except Exception as error:
            print(error)
            continue

        if df.empty:
            continue

        close = close_prices.iloc[-1]
        prev_price = close_prices.iloc[-2]
        ma200 = df.tail(200)["Close"].mean()
        ma100 = df.tail(100)["Close"].mean()
        ma50 = df.tail(50)["Close"].mean()

        data.append({
            "ticker": stock,
            "category": stocks_data[stock]["category"],
            "close": round(close, 3),
            "change": calculate_change(close, prev_price),
            "low_52": round(df["Low"].min(), 3),
            "high_52":round(df["High"].max(), 3),
            "rsi": round(calculate_rsi(close_prices)),
            "ma50": format_ma(close, ma50),
            "ma100": format_ma(close, ma100),
            "ma200": format_ma(close, ma200),
            "vol>25%": "Yes" if latest_volume > 1.25 * mean_volume else "No",
        })
    print(len(data))
    
    db.insert_stock_data(data)
            

def get_data(hard_update = False):
    stocks_data = db.get_stocks_by_category()
        
    if len(stocks_data) == 0 or hard_update is True:    
        fetch_data()
    
    stocks_data = db.get_stocks_by_category()
    # df = pd.DataFrame(stocks_data).transpose().sort_values(by=["category"])
    # dfs.append(df[["category","close", "change", "low_52", "high_52", "rsi", "ma50", "ma100", "ma200", "vol>25%"]])

    return stocks_data

def get_categories():
    categories = []

    for document in db.fetchall("category"): 
        categories.append(document["category"])

    return categories


def style_trigger(v):
    green = "background-color: #e6ffe6"
    red = "background-color: #ffe6e6"

    if type(v) == int:
        return green if v > 30 and v < 70 else red
    else:
        return green if v == "Under" or v == "Yes" else red


def style_change(v):
    green = "background-color: #e6ffe6"
    red = "background-color: #ffe6e6"

    if v > 0.05:
        return green

    if v < -0.05:
        return red

    return None


def style_dfs(dfs: list):
    for df in dfs:
        styler = (
            df.style.map(
                style_trigger, subset=["rsi", "ma50", "ma100", "ma200", "vol>25%"]
            )
            .format(precision=3, subset=["close", "low_52", "high_52"])
            .format("{:,.2%}", subset="change")
            .map(style_change, subset="change")
            .set_table_attributes('class="table is-bordered is-striped is-hoverable"')
        )

    return styler.to_html();
