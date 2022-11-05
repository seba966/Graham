import bs4 as bs
import pandas as pd
import re
from datetime import date
import requests
import db_connection as db
import download_scrap as dw
from json.decoder import JSONDecodeError


def shares_outstanding(ticker):
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                        'CommonStockSharesOutstanding.json'.format(cik),
                        headers=headers)
    resp2 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/dei/'
                         'EntityCommonStockSharesOutstanding.json'.format(cik),
                         headers=headers)
    resp3 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                         'WeightedAverageNumberOfSharesOutstandingBasic.json'.format(cik),
                         headers=headers)
    flag = 1
    flag2 = 1
    flag3 = 1
    years = []
    shares_outstanding_values = []
    try:
        json_data = resp.json()['units']['shares']
        # print("jest zwykly")
    except JSONDecodeError:
        flag = 0
    try:
        json_data2 = resp2.json()['units']['shares']
        # print("jest entity")
    except JSONDecodeError:
        flag2 = 0
    try:
        json_data3 = resp3.json()['units']['shares']
        # print("jest basic")
    except JSONDecodeError:
        flag3 = 0

    if flag == 1 and flag2 == 1:
        if len(json_data2) > len(json_data):
            json_data = json_data2
        if flag3 == 1 and (len(json_data3) > len(json_data)):
            json_data = json_data3

    elif flag == 0 and flag2 == 1:
        json_data = json_data2
        if flag3 == 1 and (len(json_data3) > len(json_data)):
            json_data = json_data3

    elif flag == 0 and flag2 == 0 and flag3 == 1:
        json_data = json_data3

    if flag == 1 or flag2 == 1 or flag3 == 1:
        for element in json_data:
            if element['form'] == '10-K' or element['form'] == '10-K/A':
                if element['end'][:4] not in years:
                    years.append(element['end'][:4])
                    shares_outstanding_values.append(element['val'])

    else:
        pass
        # print("nic nie bylo")

    shares_outstanding_data = pd.DataFrame(data={'shares_outstanding': shares_outstanding_values},
                                           index=pd.Series(years, name='year', dtype='Int64'))
    shares_outstanding_data = shares_outstanding_data.drop(
        shares_outstanding_data[shares_outstanding_data.index < 2010].index)

    return shares_outstanding_data


def so_check(ticker):
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                        'CommonStockSharesOutstanding.json'.format(cik),
                        headers=headers)

    resp2 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/dei/'
                         'EntityCommonStockSharesOutstanding.json'.format(cik),
                         headers=headers)

    resp3 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/dei/'
                         'WeightedAverageNumberOfSharesOutstandingBasic.json'.format(cik),
                         headers=headers)

    print('---{}---'.format(ticker))
    try:
        json_data = resp.json()['units']['shares']
        print("jest zwykly")
    except JSONDecodeError:
        print("nie ma zwykly")
    try:
        json_data2 = resp2.json()['units']['shares']
        # print("jest entity")
    except JSONDecodeError:
        print("nie ma entity")
    try:
        if len(json_data) > len(json_data2):
            print("+++zwykly wiekszy od entity+++")
    except:
        print('error')


def shares_outstanding_split_included(ticker):
    shares_outstanding_data = shares_outstanding(ticker)
    stock_splits_data = dw.stock_splits(ticker)
    stock_splits_data = stock_splits_data.drop(stock_splits_data[stock_splits_data.index < '2008-01-01'].index)
    years = []
    values = []
    for index, row in shares_outstanding_data.iterrows():
        years.append(index)
        value = row['shares_outstanding']
        for index_c, row_c in stock_splits_data.iterrows():
            if int(index) < index_c.year:
                value = value * row_c['split']
        values.append(int(value))
    shares_outstanding_split_included_data = pd.DataFrame(data={'shares_outstanding_split_inc': values},
                                                          index=pd.Series(years, name='year', dtype='Int64'))

    return shares_outstanding_split_included_data


def net_income_check(ticker):
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/NetIncomeLoss.json'.format(cik),
                        headers=headers)

    resp2 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                         'NetIncomeLossAvailableToCommonStockholdersBasic.json'.format(cik),
                         headers=headers)

    print('---{}---'.format(ticker))
    try:
        json_data = resp.json()['units']['USD']
        print("jest NetIncomeLoss")
    except JSONDecodeError:
        print("nie ma NetIncomeLoss")
    try:
        json_data2 = resp2.json()['units']['USD']
        print("jest NetIncomeLossAvailableToCommonStockholdersBasic")
    except JSONDecodeError:
        print("nie ma NetIncomeLossAvailableToCommonStockholdersBasic")
    try:
        if len(json_data) > len(json_data2):
            print("+++NetIncomeLoss wiekszy od NetIncomeLossAvailableToCommonStockholdersBasic+++")
    except:
        print('error')


def net_income(ticker):
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                        'NetIncomeLossAvailableToCommonStockholdersBasic.json'.format(cik),
                        headers=headers)
    resp2 = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                         'NetIncomeLoss.json'.format(cik),
                         headers=headers)
    years = []
    net_income_values = []
    years2 = []
    net_income_values2 = []
    flag = 1
    flag2 = 1
    net_income_data = pd.DataFrame(data={'net_income': net_income_values},
                                   index=pd.Series(years, name='year', dtype='Int64'))
    try:
        json_data = resp.json()['units']['USD']
        for element in json_data:
            if 'frame' in element.keys() and len(element['frame']) == 6:
                year = element['frame'][2:]
                value = element['val']
                years.append(year)
                net_income_values.append(value)
        net_income_data = pd.DataFrame(data={'net_income': net_income_values},
                                       index=pd.Series(years, name='year', dtype='Int64'))
    except JSONDecodeError:
        flag = 0
    try:
        json_data2 = resp2.json()['units']['USD']
        for element in json_data2:
            if 'frame' in element.keys() and len(element['frame']) == 6:
                year = element['frame'][2:]
                value = element['val']
                years2.append(year)
                net_income_values2.append(value)
        net_income_data2 = pd.DataFrame(data={'net_income': net_income_values2},
                                        index=pd.Series(years2, name='year', dtype='Int64'))
    except JSONDecodeError:
        flag2 = 0
    if flag == 1 and flag2 == 1:
        if len(net_income_data2) > len(net_income_data):
            net_income_data = net_income_data2
    elif flag == 0 and flag2 == 1:
        net_income_data = net_income_data2
    elif flag == 0 and flag2 == 0:
        try:
            resp = requests.get('https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/'
                                'ProfitLoss.json'.format(cik),
                                headers=headers)
            json_data = resp.json()['units']['USD']
            for element in json_data:
                if 'frame' in element.keys() and len(element['frame']) == 6:
                    year = element['frame'][2:]
                    value = element['val']
                    years.append(year)
                    net_income_values.append(value)
            net_income_data = pd.DataFrame(data={'net_income': net_income_values},
                                           index=pd.Series(years, name='year', dtype='Int64'))
        except JSONDecodeError:
            print('probably no xbrl')
    net_income_data = net_income_data.drop(
        net_income_data[net_income_data.index < 2010].index)
    net_income_data = net_income_data.drop(
        net_income_data[net_income_data.index == str(date.today().year)].index)

    return net_income_data


def stockholders_equity(ticker):
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(
        'https://data.sec.gov/api/xbrl/companyconcept/CIK{}'
        '/us-gaap/StockholdersEquity.json'.format(cik),
        headers=headers)
    resp2 = requests.get(
        'https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap'
        '/StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest.json'.format(cik),
        headers=headers)
    years = []
    stockholders_equity_values = []
    flag = 1
    flag2 = 1
    try:
        json_data = resp.json()['units']['USD']
    except JSONDecodeError:
        # print("nie ma krotszego")
        flag = 0
    try:
        json_data2 = resp2.json()['units']['USD']
    except JSONDecodeError:
        # print("nie ma dluzszego")
        flag2 = 0

    if flag == 1 and flag2 == 1:
        for element in json_data:
            if element['form'] == '10-K' or element['form'] == '10-K/A':
                if element['end'][:4] not in years:
                    years.append(element['end'][:4])
                    stockholders_equity_values.append(element['val'])
        for element in json_data2:
            if element['form'] == '10-K' or element['form'] == '10-K/A':
                if element['end'][:4] not in years:
                    years.append(element['end'][:4])
                    stockholders_equity_values.append(element['val'])
    elif flag == 1 and flag2 == 0:
        for element in json_data:
            if element['form'] == '10-K' or element['form'] == '10-K/A':
                if element['end'][:4] not in years:
                    years.append(element['end'][:4])
                    stockholders_equity_values.append(element['val'])
    elif flag == 0 and flag2 == 1:
        for element in json_data2:
            if element['form'] == '10-K' or element['form'] == '10-K/A':
                if element['end'][:4] not in years:
                    years.append(element['end'][:4])
                    stockholders_equity_values.append(element['val'])
    else:
        print("nie bylo nic w stockholders equity")
        stockholders_equity_data = pd.DataFrame(data={'stockholders_equity': stockholders_equity_values},
                                                index=pd.Series(years, name='year', dtype='Int64'))
    stockholders_equity_data = pd.DataFrame(data={'stockholders_equity': stockholders_equity_values},
                                            index=pd.Series(years, name='year', dtype='Int64'))
    stockholders_equity_data = stockholders_equity_data.sort_index()
    stockholders_equity_data = stockholders_equity_data.drop(
        stockholders_equity_data[stockholders_equity_data.index < 2010].index)

    return stockholders_equity_data


def eps_basic_and_diluted(ticker):  # dziwne wartości
    sp500 = db.get_sp500()
    cik = sp500['cik'].loc[sp500['ticker'] == '{}'.format(ticker)].tolist()[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp_b = requests.get(
        'https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/EarningsPerShareBasic.json'.format(cik),
        headers=headers)
    resp_d = requests.get(
        'https://data.sec.gov/api/xbrl/companyconcept/CIK{}/us-gaap/EarningsPerShareDiluted.json'.format(cik),
        headers=headers)
    json_data_b = resp_b.json()['units']['USD/shares']
    json_data_d = resp_d.json()['units']['USD/shares']
    years_b = []
    years_d = []
    eps_basic_values = []
    eps_diluted_values = []
    for element in json_data_b:
        if 'frame' in element.keys() and len(element['frame']) == 6:
            year = element['frame'][2:]
            value = element['val']
            years_b.append(year)
            eps_basic_values.append(value)
    for element in json_data_d:
        if 'frame' in element.keys() and len(element['frame']) == 6:
            year = element['frame'][2:]
            value = element['val']
            years_d.append(year)
            eps_diluted_values.append(value)
    eps_basic_data = pd.DataFrame(data={'eps_basic': eps_basic_values},
                                  index=pd.Series(years_b, name='year', dtype='Int64'))
    eps_diluted_data = pd.DataFrame(data={'eps_diluted': eps_diluted_values},
                                    index=pd.Series(years_d, name='year', dtype='Int64'))
    eps_data = eps_basic_data.join(eps_diluted_data)
    eps_data = eps_data.drop(
        eps_data[eps_data.index < 2010].index)

    return eps_data


def eps_split_included(ticker):
    eps_data = eps_basic_and_diluted(ticker)
    stock_splits_data = dw.stock_splits(ticker)
    stock_splits_data = stock_splits_data.drop(stock_splits_data[stock_splits_data.index < '2008-01-01'].index)
    years = []
    values_b = []
    values_d = []
    for index, row in eps_data.iterrows():
        years.append(index)
        value_b = row['eps_basic']
        value_d = row['eps_diluted']
        for index_c, row_c in stock_splits_data.iterrows():
            # if  and int(index) < index_c.year
            if int(index) < index_c.year - 2:
                value_b = value_b / row_c['split']
                value_d = value_d / row_c['split']
        values_b.append(value_b)
        values_d.append(value_d)
    if date.today().year in stock_splits_data.index.year:
        values_b[-1] = values_b[-1] / stock_splits_data['split'][-1]
        values_d[-1] = values_d[-1] / stock_splits_data['split'][-1]
        values_b[-2] = values_b[-2] / stock_splits_data['split'][-1]
        values_d[-2] = values_d[-2] / stock_splits_data['split'][-1]
    eps_split_included_data = pd.DataFrame(data={'eps_b_split_inc': values_b, 'eps_d_split_inc': values_d},
                                           index=pd.Series(years, name='year', dtype='Int64'))

    return eps_split_included_data
