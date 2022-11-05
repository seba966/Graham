import bs4 as bs
import pandas as pd
import yfinance as yf
import re
import html5lib
from datetime import date, datetime
import requests
import db_connection as db
from json.decoder import JSONDecodeError


def sp500_tickers_and_ciks():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    cik_numbers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = re.sub('\s+', '', ticker)
        cik = row.findAll('td')[7].text
        cik = re.sub('\s+', '', cik)
        tickers.append(ticker)
        cik_numbers.append(cik)
    sp500_series = pd.Series(data=cik_numbers, index=pd.Series(tickers, name='ticker'), name='cik')

    return sp500_series


def company_balance_sheet(ticker):
    yf_ticker = yf.Ticker(ticker)
    balance_sheet = yf_ticker.balance_sheet

    return balance_sheet


def get_company_info(ticker):
    ticker = ticker.replace('.', '-')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(
        'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}'
        '?modules=balanceSheetHistoryQuarterly%2CfinancialData%2CdefaultKeyStatistics'.format(ticker),
        headers=headers)
    json_data = resp.json()['quoteSummary']['result'][0]
    default_key_statistics = json_data['defaultKeyStatistics']
    balance_sheet_last_quarter = json_data['balanceSheetHistoryQuarterly']['balanceSheetStatements']
    financial_data = json_data['financialData']

    market_cap = (financial_data['currentPrice']['raw'] * default_key_statistics['sharesOutstanding']['raw'])
    enterprise_value = default_key_statistics['enterpriseValue']['raw']
    current_price = financial_data['currentPrice']['raw']
    shares_outstanding = default_key_statistics['sharesOutstanding']['raw']
    try:
        current_assets = balance_sheet_last_quarter[0]['totalCurrentAssets']['raw']
    except KeyError:
        current_assets = balance_sheet_last_quarter[1]['totalCurrentAssets']['raw']
    try:
        current_liabilities = balance_sheet_last_quarter[0]['totalCurrentLiabilities']['raw']
    except KeyError:
        current_liabilities = balance_sheet_last_quarter[1]['totalCurrentLiabilities']['raw']
    try:
        long_term_debt = balance_sheet_last_quarter[0]['longTermDebt']['raw']
    except KeyError:
        try:
            long_term_debt = balance_sheet_last_quarter[1]['longTermDebt']['raw']
        except KeyError:
            long_term_debt = float('NaN')

    dictionary = {
        'market_cap': market_cap,
        'enterprise_value': enterprise_value,
        'current_price': current_price,
        'shares_outstanding': shares_outstanding,
        'current_assets': current_assets,
        'current_liabilities': current_liabilities,
        'long_term_debt': long_term_debt
    }
    df = pd.DataFrame(data=dictionary, index=pd.Series(date.today(), name='date'))

    return df


def company_share_dividend_split_history(ticker):
    # url = 'https://query2.finance.yahoo.com/v8/finance/chart/
    # AAPL?symbol=AAPL&period1=0&period2=9999999999&interval=1d&events=div%7Csplit'
    ticker = ticker.replace('.', '-')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.102 Safari/537.36'}
    resp = requests.get(
        'https://query2.finance.yahoo.com/v8/finance/chart/{}'
        '?symbol={}&period1=0&period2=9999999999&interval=1d&events=div%7Csplit'.format(ticker, ticker),
        headers=headers)
    json_data = resp.json()['chart']['result'][0]
    dates = [date.fromtimestamp(x) for x in json_data['timestamp']]
    dictionary = {
        'open': json_data['indicators']['quote'][0]['open'],
        'close': json_data['indicators']['quote'][0]['close'],
        'adjclose': json_data['indicators']['adjclose'][0]['adjclose'],
        'high': json_data['indicators']['quote'][0]['high'],
        'low': json_data['indicators']['quote'][0]['low'],
        'volume': json_data['indicators']['quote'][0]['volume']
    }
    share_df = pd.DataFrame(data=dictionary, index=pd.Series(dates, name='date'))

    try:
        dividend_dates = [date.fromtimestamp(int(x)) for x in json_data['events']['dividends'].keys()]
        dividend_values = [x['amount'] for x in json_data['events']['dividends'].values()]
    except KeyError:
        dividend_dates = []
        dividend_values = []
    dividend_df = pd.DataFrame(data={'dividend': dividend_values}, index=pd.Series(dividend_dates, name='date'))

    try:
        split_dates = [date.fromtimestamp(int(x)) for x in json_data['events']['splits'].keys()]
        split_values = [x['splitRatio'] for x in json_data['events']['splits'].values()]
    except KeyError:
        split_dates = []
        split_values = []
    split_df = pd.DataFrame(data={'split': split_values}, index=pd.Series(split_dates, name='date'))

    return share_df, dividend_df, split_df


def get_annual_share_return(ticker):
    data = company_share_dividend_split_history(ticker)[0]['close']
    firsts_and_lasts = []
    firsts = []
    lasts = []
    data_index_years = list(dict.fromkeys([x.year for x in data.index]))
    for year_el in data_index_years:
        for date_el in data.index:
            if date_el.year == year_el:
                if date_el.month == 1:
                    firsts.append(date_el)
                elif date_el.month == 12:
                    lasts.append(date_el)
        if len(firsts) > 0 and len(lasts) > 0:
            firsts_and_lasts.append(min(firsts))
            firsts_and_lasts.append(max(lasts))
            firsts = []
            lasts = []
    data = data.filter(items=firsts_and_lasts, axis=0)
    years = []
    return_values = []
    prev_value_el = None
    i = 0
    for date_el, value_el in zip(data.index, data):
        if i % 2 != 0:
            years.append(date_el.year)
            return_value = ((value_el - prev_value_el) / prev_value_el) * 100
            return_value = round(return_value, 2)
            return_values.append(return_value)
        else:
            prev_value_el = value_el
        i += 1
    # annual_return_data = pd.Series(data=return_values, index=pd.Series(years, name='year', dtype='Int64'),
    #                                name='annual_return')
    annual_return_data = pd.DataFrame(data={'annual_return': return_values}, index=pd.Series(years, name='year'))

    return annual_return_data


# def dividends_paid(ticker):
#     data = company_share_history(ticker)[1]['dividend']
#     dividends_data = data.loc[data != 0]
#     dividends_data = dividends_data.rename('dividend')
#     dividends_data.index.name = 'date'
#
#     return dividends_data


# def stock_splits(ticker):
#     data = yf.Ticker(ticker).splits.rename('split')
#     data.index.name = 'date'
#     stock_split_data = data.to_frame()
#     stock_split_data = stock_split_data.drop(
#         stock_split_data[stock_split_data.index < '2010-01-01'].index)
#
#     return stock_split_data


# def get_company_info2(ticker):
#     yf_ticker = yf.Ticker(ticker)
#     info = yf_ticker.info
#     market_cap = info['marketCap']
#     enterprise_value = info['enterpriseValue']
#     current_price = info['currentPrice']
#     shares_outstanding = info['sharesOutstanding']
#     q_balance_sheet = yf_ticker.quarterly_balance_sheet
#     try:
#         current_assets = q_balance_sheet.loc['Total Current Assets'].values[0]
#     except KeyError:
#         current_assets = float("NaN")
#     try:
#         current_liabilities = q_balance_sheet.loc['Total Current Liabilities'].values[0]
#     except KeyError:
#         current_liabilities = float("NaN")
#     try:
#         long_term_debt = q_balance_sheet.loc['Long Term Debt'].values[0]
#     except KeyError:
#         long_term_debt = float("NaN")
#     dict_data = {'market_cap': market_cap, 'enterprise_value': enterprise_value, 'current_price': current_price,
#                  'shares_outstanding': shares_outstanding, 'current_assets': current_assets,
#                  'current_liabilities': current_liabilities, 'long_term_debt': long_term_debt}
#     df = pd.DataFrame(data=dict_data, index=pd.Series(date.today(), name='date'))
#
#     return df

# def all_company_data(ticker, period="max", interval="1d"):
#     yf_ticker = yf.Ticker(ticker)
#     info = yf_ticker.info
#     balance_sheet = yf_ticker.balance_sheet
#     q_balance_sheet = yf_ticker.quarterly_balance_sheet
#     share_history = yf_ticker.history(period=period, interval=interval)
#
#     return info, balance_sheet, q_balance_sheet, share_history

# def company_balance_sheet_essentials(ticker):
#     data = company_q_balance_sheet(ticker)
#     current_assets = data.loc['Total Current Assets'].values[0]
#     current_liabilities = data.loc['Total Current Liabilities'].values[0]
#     long_term_debt = data.loc['Long Term Debt'].values[0]
#     dict_data = {'current_assets': current_assets, 'current_liabilities': current_liabilities,
#                  'long_term_debt': long_term_debt}
#
#     return dict_data


# def company_q_balance_sheet(ticker):
#     yf_ticker = yf.Ticker(ticker)
#     q_balance_sheet = yf_ticker.quarterly_balance_sheet
#
#     return q_balance_sheet
