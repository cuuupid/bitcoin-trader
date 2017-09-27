import sys
import os
import re
import datetime as dt


def get_24h_feed():
    f = open('ether_24h_latest.csv', 'r')
    feed = []
    for line in f.readlines():
        feed.append(float(line.split(',')[1]))
    f.close()
    return feed


def get_yesterday_data():
    f = open('ether_24h_latest.csv', 'r')
    feed = []
    for line in f.readlines():
        feed.append(float(line.split(',')[1]))
    f.close()
    y_d = {}
    y_d['close'] = feed[-1]
    feed.sort()
    y_d['high'] = feed[-1]
    y_d['low'] = feed[0]
    return y_d


def backtest_algo(api, algo_name):
    algo_name = re.sub('[^a-zA-Z_]', '', algo_name.replace('-', '_'))
    try:
        from algo.algo_name import run
        yesterday_data = []
        feed = []
        run(yesterday_data, feed)
    except Exception as e:
        return None


def backtest_test(feed, yesterday_data):
    from algo.pivot_point import run
    return run(yesterday_data, feed)


import json


def backtest_demo_quandl_amzn():
    def calculate_pivots(high, low, close):
        H, L, C = [high, low, close]
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

    amzn_data = json.load(open('amzn.json', 'r'))
    print("[+] Loaded Amazon Data, most recent point: " +
          amzn_data['datatable']['data'][-1][0])
    print("[=] Calculating pivots...")
    for datapoint in amzn_data['datatable']['data'][-14:]:
        pivots = calculate_pivots(datapoint[1], datapoint[2], datapoint[3])
        print("-" * 100)
        print("Pivots for: " + datapoint[0])
        p4(pivots)