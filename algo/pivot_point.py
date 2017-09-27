import sys
import os


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




def calc_boundary_crossed(pivot_list, price):
    if price > pivot_list[-1]:
        return len(pivot_list) - 1
    if price < pivot_list[0]:
        return 0
    new_list = pivot_list.copy()
    new_list.append(price)
    new_list.sort()
    price_index = new_list.index(price)
    return [price_index - 1, price_index]


def run(yesterday_data, feed):
    balance = {'usd': 1000.0, 'eth': 0.0, 'networth': 1000.0}

    def print_pivots(pivot_list):
        print("==== PIVOTS ====")
        pivot_order = ['S3', 'S2', 'S1', 'PP', 'R1', 'R2', 'R3']
        for x in range(len(pivot_list)):
            print("\t" + pivot_order[x] + ": " + str(pivot_list[x]))
        print("================")

    def networth(balance, price):
        return balance['usd'] + (balance['eth'] / price)
    start_worth = networth(balance, feed[0])
    print("[*] Starting with $" + str(start_worth))

    def sell(price, balance, weight=1):
        convertable = float(balance['eth'] * weight)
        balance['usd'] += convertable / price
        balance['eth'] -= convertable
        print("[-] Sold " + str(convertable) + " ethereum for " +
              str(convertable / price) + " USD")
        print("\tBalance: " + str(networth(balance, price)))
        print("\tEarnings: " + str(networth(balance, price) - start_worth))
        balance['networth'] = networth(balance, price)
        return balance, -1

    def buy(price, balance, weight=1):
        convertable = float(balance['usd'] * weight)
        balance['eth'] += convertable * price
        balance['usd'] -= convertable
        print("[+] Bought " + str(convertable * price) +
              " ethereum for " + str(convertable) + " USD")
        print("\tBalance: " + str(networth(balance, price)))
        print("\tEarnings: " + str(networth(balance, price) - start_worth))
        balance['networth'] = networth(balance, price)
        return balance, 1
    high = yesterday_data['high']
    low = yesterday_data['low']
    close = yesterday_data['close']
    pivot_dict = calculate_pivots(high, low, close)
    pivot_list = pivot_dict['s'] + [pivot_dict['pp']] + pivot_dict['r']
    print_pivots(pivot_list)
    prevBounds = [None, None]
    bounds = [None, None]
    lastAction = -1
    cur_balance, cur_lastAction = [{'usd': 0, 'eth': 0, 'networth': 0}, 0]
    for price in feed:
        bounds = calc_boundary_crossed(pivot_list, price)
        if prevBounds[0] != None:
            if bounds[0] <= prevBounds[1] and bounds[1] > 3 and lastAction > 0:
                cur_balance, cur_lastAction = sell(price, balance)
                if cur_balance['networth'] > balance['networth']:
                    print("[=] Updated balance")
                    balance, lastAction = [cur_balance, cur_lastAction]
                else:
                    print("--- Discarding last balance")
            elif bounds[1] >= prevBounds[0] and bounds[0] < 3 and lastAction < 0:
                cur_balance, cur_lastAction = buy(price, balance)
                if cur_balance['networth'] > balance['networth']:
                    print("[=] Updated balance")
                    balance, lastAction = [cur_balance, cur_lastAction]
                else:
                    print("--- Discarding last balance")
        prevBounds = bounds
    profit = networth(balance, feed[-1]) - start_worth
    print("-" * 30)
    print("[*] Concluded run, ended with profit: $" + str(profit))
    return profit
