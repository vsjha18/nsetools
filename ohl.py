#!/usr/bin/env python
import requests
import json
import ast
import re
import os
import pandas as pd
import datetime as dt
import pickle
from argparse import ArgumentParser
from pprint import pprint

INVESTMENT_AMOUNT = 10000
URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json"
# URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/bankNiftyStockWatch.json"
# URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json"
filter = ["open", "high", "low", "last", "graph"]

drop_columns = ['cAct', 'mPC', 'mVal', 'ntP', 'per',
                'ptsC', 'trdVol', 'trdVolM', 'wkhicm_adj',
                'wklocm_adj', 'xDt', 'yPC', 'wkhi', 'wklo']

# create data dir if not available
file_path = os.path.realpath(__file__)
dirname = os.path.dirname(file_path)
data_dir_path = os.path.join(dirname, "__data__")
todays_dir_path = os.path.join(data_dir_path, dt.date.today().isoformat())

if not os.path.exists(data_dir_path):
    # create data dir
    try:
        os.mkdir(data_dir_path)
    except Exception as err:
        print("make sure %s is writable: %s" % (dirname, str(err)))

if not os.path.exists(todays_dir_path):
    # create today's dir
    try:
        os.mkdir(todays_dir_path)
    except Exception as err:
        print("make sure %s is writable: %s" % (todays_dir_path, str(err)))

parser = ArgumentParser(
    description='daytrading tool')

parser.add_argument("-c", "--cat", action="store", help="provide category - fo, nifty, banks", default="fo")
parser.add_argument("-s", "--snap", action="store", help="provide snap name")
parser.add_argument("-bt", "--backtest", action="store", help="provide snap name to backtest")

cli = parser.parse_args()

if cli.cat == "fo":
    URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json"
elif cli.cat == "banks":
    URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/bankNiftyStockWatch.json"
elif cli.cat == "nifty":
    URL = "https://nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json"
else:
    print("provide proper category")
    exit(1)

def download_data(url, fake=False):
    """download the raw data from web api"""
    if fake:
        return pickle.load(open("sample_data.pcl", "rb"))
    else:
        res = requests.get(url)
        string_response = res.content.decode("utf-8")
        dict_response = ast.literal_eval(string_response)
        return dict_response["data"]

def prepare_data(data):
    """return a dataframe after
        1. cleaning server response
        2. creating and reindexing dataframe.
    """
    for idx, value in enumerate(data):
        data[idx] = clean_server_response(value)

    # this method of loading dataframe helps in case where we have list
    # of dictionaries and we want all the dict keys to column headers.
    stocks = pd.DataFrame.from_records(data).set_index('symbol')

    # drop few columns.
    stocks.drop(drop_columns, axis=1, inplace=True)

    # re-order columns.
    stocks = stocks.reindex(['open', 'high', 'low', 'ltP'], axis=1)
    stocks.columns = ["open", "high", "low", "last"]

    return stocks

def clean_server_response(d):
    """cleans the server reponse by replacing:
        '-'     -> None
        '1,000' -> 1000
    :param resp_dict:
    """
    for key, value in d.items():
        if type(value) is str or isinstance(value, str):
            if re.match('-', value):
                value = None
            elif re.search(r'^[0-9,.]+$', value):
                # replace , to '', and type cast to int
                value = float(re.sub(',', '', value))
            else:
                value= str(value)
        d[key] = value
    return d

def get_long_stocks(stocks):
    # read this for chained indexing problems
    # https://www.dataquest.io/blog/settingwithcopywarning/
    longs = stocks.query("open==low").copy()
    longs["pir"] = ((longs["last"] - longs["low"]) * 100) / (longs["high"] - longs["low"])
    longs = longs.round(2)
    longs = longs.sort_values("pir", ascending=False)
    longs = attach_graph(longs)
    return longs

def attach_graph(df):
    for idx, row in df.iterrows():
        rnd = round(row.pir/10)
        graph = ""
        for i in range(10):
            if i == (rnd -1):
                graph = graph + "^"
            else:
                graph = graph + "."
        df.at[idx, "graph"] = graph
    return df

def get_short_stocks(stocks):
    # read this for chained indexing problems
    # https://www.dataquest.io/blog/settingwithcopywarning/
    shorts = stocks.query("open==high").copy()
    shorts["pir"] = ((shorts["high"] - shorts["last"]) * 100) / (shorts["high"] - shorts["low"])
    shorts = shorts.round(2)
    shorts = shorts.sort_values("pir", ascending=False)
    shorts = attach_graph(shorts)
    return shorts


def get_quote(symbol, stocks):
    for stock in stocks:
        if stock["symbol"] == symbol:
            return stock

def summary():
    data = download_data(URL, fake=False)
    stocks = prepare_data(data)
    longs = get_long_stocks(stocks)
    shorts = get_short_stocks(stocks)
    print("Longs: %s, Shorts: %s" % (len(longs), len(shorts)))
    print("========== LONGS ==========")
    print(longs[filter])
    print("========== SHORTS ==========")
    print(shorts[filter])
    return (stocks, longs, shorts)


def invest(stocks):
    # invest in top 5 longs and top 5 shorts
    for index, stock in stocks.iterrows():
        qty = INVESTMENT_AMOUNT / stock["last"]
        amount = qty * stock["last"]
        stocks.loc[index, "qty"] = qty
        stocks.loc[index, "amount"] = amount
    stocks = stocks.round(2)
    return stocks

def snap(name):
    all, longs, shorts = summary()
    longs_snap_name = name + "_" + "longs.pcl"
    shorts_snap_name = name + "_" + "shorts.pcl"

    longs_snap_path = os.path.join(todays_dir_path, longs_snap_name)
    shorts_snap_path = os.path.join(todays_dir_path, shorts_snap_name)
    longs = invest(longs)
    shorts = invest(shorts)
    longs.to_pickle(longs_snap_path)
    shorts.to_pickle(shorts_snap_path)
    print("snapping completed ...")

def backtest(name):
    all, longs, shorts = summary()
    longs_snap_name = name + "_" + "longs.pcl"
    shorts_snap_name = name + "_" + "shorts.pcl"
    longs_snap_path = os.path.join(todays_dir_path, longs_snap_name)
    shorts_snap_path = os.path.join(todays_dir_path, shorts_snap_name)

    # check if these exist
    if os.path.exists(longs_snap_path) and os.path.exists(shorts_snap_path):
        longs = pd.read_pickle(longs_snap_path)
        shorts = pd.read_pickle(shorts_snap_path)
        for idx, stock in all.iterrows():
            if idx in longs.index:
                if all.loc[idx, "low"] < longs.loc[idx, "low"]:
                    longs.loc[idx, "SL"] = True
                    longs.loc[idx, "PL"] = (longs.loc[idx, "low"] - longs.loc[idx, "last"]) * longs.loc[idx, "qty"]
                else:
                    longs.loc[idx, "SL"] = False
                    longs.loc[idx, "PL"] = (all.loc[idx, "last"] - longs.loc[idx, "last"]) * longs.loc[idx, "qty"]
            if idx in shorts.index:
                if all.loc[idx, "high"] > shorts.loc[idx, "high"]:
                    shorts.loc[idx, "SL"] = True
                    shorts.loc[idx, "PL"] = (shorts.loc[idx, "last"] - shorts.loc[idx, "high"]) * shorts.loc[idx, "qty"]
                else:
                    shorts.loc[idx, "SL"] = False
                    shorts.loc[idx, "PL"] = (shorts.loc[idx, "last"] - all.loc[idx, "last"]) * shorts.loc[idx, "qty"]
        print(longs.round(2))
        print(shorts.round(2))
        print("Net P&L in LONGS = %s" % longs.PL.sum())
        print("Net P&L in SHORTS = %s" % shorts.PL.sum())
    else:
        print("snap names are wrong it seems ...")
        exit(1)
def main():
    # do this in any case
    summary()

    if cli.snap:
        snap(cli.snap)

    if cli.backtest:
        backtest(cli.backtest)

if __name__ == "__main__":
    # http://finance.google.com/finance/info?client=ig&q=NSE:HDFC
    # all, longs, shorts = summary()
    # main()

    # refactor later
    from time import sleep
    while True:
        main()
        sleep(120)


    # stocks, longs, shorts = summary()
    # invest(longs, shorts)
    # file_path = os.path.realpath(__file__)
    # print(os.path.dirname(file_path))
    # TODO: when running in continuous mode, make snaps for each.
    # TODO: show a comparative change from the last snap.
    # TODO: also show stocks which come back from their low's to the window.
    # TODO: show volume jumps from previous snap.
    # TODO: Price movement in relation to the index. This can also indicate interesting things.

