import requests
api_key = "YH11K53DK4SKWEZ9"
import numpy as np

def backtest(ticker, level=None, auto_confidence=0.13):
    response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' +
                            ticker + '&interval=5min&apikey=' + api_key)
    json_data = response.json()
    print("[=] Loaded data... last updated " +
          json_data['Meta Data']["3. Last Refreshed"])
    candles = [
        {
            'time': datapoint[0],
            'open': datapoint[1]['1. open'],
            'high': datapoint[1]['2. high'],
            'low': datapoint[1]['3. low'],
            'close': datapoint[1]['4. close'],
            'volume': datapoint[1]['5. volume']
        }
        for datapoint in list(json_data['Time Series (5min)'].items())]
    response = requests.get(
        'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=' + api_key)
    json_data = response.json()
    print("[=] Loaded data... last updated " +
          json_data['Meta Data']["3. Last Refreshed"])
    daily_data = [
        {
            'date': datapoint[0],
            'open': datapoint[1]['1. open'],
            'high': datapoint[1]['2. high'],
            'low': datapoint[1]['3. low'],
            'close': datapoint[1]['4. close'],
            'volume': datapoint[1]['5. volume']
        }
        for datapoint in list(json_data['Time Series (Daily)'].items())]
    yesterday_data = daily_data[1]  # TODO: change this to -1 in realtime
    print("[=] Basing pivots off of " + yesterday_data['date'])

    def calculate_pivots(high, low, close):
        H, L, C = [float(high), float(low), float(close)]
        PP = float(H + L + C) / 3
        R1 = (2 * PP) - L
        S1 = (2 * PP) - H
        R2 = (PP - S1) + R1
        S2 = PP - (R1 - S1)
        R3 = (PP - S2) + R2
        S3 = PP - (R2 - S2)
        return {
            'r': [
                R1, R2, R3
            ],
            's': [
                S3, S2, S1
            ],
            'pp': PP
        }

    def p4(pivots):
        print("\tR3: " + str(pivots['r'][-1]))
        print("\tR2: " + str(pivots['r'][-2]))
        print("\tR1: " + str(pivots['r'][-3]))
        print("\tPP: " + str(pivots['pp']))
        print("\tS1: " + str(pivots['s'][-1]))
        print("\tS2: " + str(pivots['s'][-2]))
        print("\tS3: " + str(pivots['s'][-3]))
        return pivots['s'] + [pivots['pp']] + pivots['r']

    pivots = calculate_pivots(
        yesterday_data['high'], yesterday_data['low'], yesterday_data['close'])

    pretty_pivots = p4(pivots)
    if not level: 
        level=np.std(pretty_pivots) * auto_confidence
        print("Auto calculated level: "+str(level))
    print("Pivot for the day: "+str(pretty_pivots[3]))
    input("Press ENTER to continue . . .")
    for candle in candles:
        p_ind = 0
        for pivot_point in pretty_pivots:
            if abs(float(candle['close']) - pivot_point) < level:
                print("[+] At " + candle['time'] + ", we were at " + ('support of ' if p_ind < 3 else 'resistance of ' if p_ind >
                                                                      3 else 'pivot of ') + str(pivot_point) + ' (trading at ' + candle['close'] + ')')
            p_ind = p_ind + 1