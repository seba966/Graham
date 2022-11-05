import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from functools import reduce
import pandas_datareader.data as web
from pandas.api.types import CategoricalDtype
from selenium import webdriver
import bs4 as bs
from webdriver_manager.firefox import GeckoDriverManager

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}


def get_income_statement(ticker):
    url_is = 'https://www.macrotrends.net/stocks/charts/{}/something/income-statement'.format(ticker)
    df_is = get_dataframe(url_is).rename(columns={'eps_earnings_per_share': 'diluted_eps'})

    return df_is


def get_balance_sheet(ticker):
    url_bs = 'https://www.macrotrends.net/stocks/charts/{}/some/balance-sheet'.format(ticker)
    df_bs = get_dataframe(url_bs)

    return df_bs


def get_cash_flow_statement(ticker):
    url_cfs = 'https://www.macrotrends.net/stocks/charts/{}/some/cash-flow-statement'.format(ticker)
    df_cfs = get_dataframe(url_cfs)

    return df_cfs


def get_financial_ratios(ticker):
    url_fr = 'https://www.macrotrends.net/stocks/charts/{}/some/financial-ratios'.format(ticker)
    df_fr = get_dataframe(url_fr)

    return df_fr


def get_dataframe(url):
    resp = requests.get(url, headers=headers)
    fin_data = re.findall('originalData = .*;', resp.text)[0][15:][:-1]
    fin_data = re.sub('<[^>]*>', '', fin_data)
    fin_data = re.sub('"popup_icon":"",', '', fin_data)
    fin_json = json.loads(fin_data)
    dfs = []
    for el in fin_json:
        field_name = el['field_name'].lower().replace(" - ", "_").replace("/", "_").replace(" ", "_").replace("&", "_")\
            .replace("-", "").replace(",", "").replace("(", "").replace(")", "").replace("___", "_").replace("__", "_")
        del el['field_name']
        df = pd.DataFrame.from_dict(el, orient='index', columns=[field_name])
        df = df.replace('', np.nan)
        df[field_name] = df[field_name].astype(float) * 1000000
        df.dropna(how='all', inplace=True)
        years = []
        new_dates = []
        for date in df.index:
            if (date[:4] in years) and (len(new_dates) > 1) and (date[6:] == new_dates[-2][6:]):
                new_dates[-1] = date
            elif date[:4] in years:
                continue
            else:
                years.append(date[:4])
                new_dates.append(date)
        df = df.loc[new_dates]
        df = df.iloc[::-1]
        df.index.rename('date', inplace=True)
        dfs.append(df)
    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['date'], how='left'), dfs)
    df_merged.index = [int(index[:4]) for index in df_merged.index]
    df_merged.index.rename('year', inplace=True)

    return df_merged


# def get_ticker_url(ticker):
#     driver = webdriver.Firefox(executable_path='D:\Programowanie\geckodriver.exe')
#     url = 'https://www.macrotrends.net/'
#     url2 = 'https://www.macrotrends.net/stocks/charts/{}/something/financial-statements'.format(ticker)
#     driver.get(url)
#     box = driver.find_element(By.CSS_SELECTOR, ".js-typeahead")
#     box.send_keys(ticker)
#     time.sleep(1)
#     box.send_keys(Keys.DOWN, Keys.RETURN)
#     time.sleep(1)
#     geturl = driver.current_url
#     # print(geturl)
#     time.sleep(3)
#     driver.quit()
#     if "stocks" in geturl:
#         geturlsp = geturl.split("/", 10)
#         geturlf = url+"stocks/charts/"+geturlsp[5]+"/"+geturlsp[6]+"/"
#         # driver = webdriver.Firefox(executable_path='D:\Programowanie\geckodriver.exe')
#         fsurl = geturlf + "financial-statements"
#         driver.get(fsurl)
#         # time.sleep(3)
#         # driver.quit()
#         return fsurl
#     else:
#         return None

    # for col in dm.get_income_statement(ticker).columns:
    #     print(col, 'REAL,')
    # print('----------------------------------------')
    # for col in dm.get_balance_sheet(ticker).columns:
    #     print(col, 'REAL,')
    # print('----------------------------------------')
    # for col in dm.get_cash_flow_statement(ticker).columns:
    #     print(col, 'REAL,')
    # print('----------------------------------------')
    # for col in dm.get_financial_ratios(ticker).columns:
    #     print(col, 'REAL,')