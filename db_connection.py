import sqlite3
import download_scrap as dw
import pandas as pd
import download_macrotrends as dm
import download_scrap as ds


def update_sp500():
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM sp500')
    data = dw.sp500_tickers_and_ciks()
    data.to_sql('sp500', connection, if_exists='append')

    connection.close()


def get_sp500():
    connection = sqlite3.connect("graham.db")
    sp500_data = pd.read_sql('select * from sp500', connection)
    connection.close()

    return sp500_data


def update_company_info():
    print("Updating company_info table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM company_info')
    i = 1
    for ticker in ticker_list:
        data = ds.get_company_info(ticker)
        data['ci_ticker'] = ticker
        data.to_sql('company_info', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_company_info():
    connection = sqlite3.connect("graham.db")
    company_info_data = pd.read_sql("select * from company_info", connection)
    connection.close()

    return company_info_data


def get_by_ticker_company_info(ticker):
    connection = sqlite3.connect("graham.db")
    company_info_data = pd.read_sql("select * from company_info where ci_ticker = '{}'".format(ticker),
                                    connection)
    connection.close()

    return company_info_data


def update_annual_share_return():
    print("Updating company_info table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM annual_share_return')
    i = 1
    for ticker in ticker_list:
        data = ds.get_annual_share_return(ticker)
        data['asr_ticker'] = ticker
        data.to_sql('annual_share_return', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def continue_annual_share_return():
    print("Continuing to update annual_share_return table...")
    df = get_annual_share_return()
    last_ticker = df['asr_ticker'].tolist()[-1]
    ticker_list = get_sp500()['ticker'].tolist()
    ticker_index = ticker_list.index(last_ticker)
    tickers_continuation = ticker_list[ticker_index + 1:]
    connection = sqlite3.connect("graham.db")
    i = ticker_index + 2
    for ticker in tickers_continuation:
        data = ds.get_annual_share_return(ticker)
        data['asr_ticker'] = ticker
        data.to_sql('annual_share_return', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_annual_share_return():
    connection = sqlite3.connect("graham.db")
    annual_share_return_data = pd.read_sql("select * from annual_share_return", connection)
    connection.close()

    return annual_share_return_data


def get_by_ticker_annual_share_return(ticker):
    connection = sqlite3.connect("graham.db")
    annual_share_return_data = pd.read_sql("select * from annual_share_return where asr_ticker = '{}'".format(ticker),
                                           connection)
    connection.close()

    return annual_share_return_data


def update_dividends_paid():
    print("Updating dividends_paid table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM dividends_paid')
    i = 1
    for ticker in ticker_list:
        data = ds.company_share_dividend_split_history(ticker)[1]
        data['d_ticker'] = ticker
        data.to_sql('dividends_paid', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def continue_dividends_paid():
    print("Continuing to update dividends_paid table...")
    df = get_dividends_paid()
    last_ticker = df['d_ticker'].tolist()[-1]
    ticker_list = get_sp500()['ticker'].tolist()
    ticker_index = ticker_list.index(last_ticker)
    tickers_continuation = ticker_list[ticker_index + 1:]
    connection = sqlite3.connect("graham.db")
    i = ticker_index + 2
    for ticker in tickers_continuation:
        data = ds.company_share_dividend_split_history(ticker)[1]
        data['d_ticker'] = ticker
        data.to_sql('dividends_paid', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_dividends_paid():
    connection = sqlite3.connect("graham.db")
    dividends_paid_data = pd.read_sql("select * from dividends_paid", connection)
    connection.close()

    return dividends_paid_data


def get_by_ticker_dividends_paid(ticker):
    connection = sqlite3.connect("graham.db")
    dividends_paid_data = pd.read_sql("select * from dividends_paid where d_ticker = '{}'".format(ticker),
                                      connection)
    connection.close()

    return dividends_paid_data


def update_income_statement():
    print("Updating income_statement table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM income_statement')
    i = 1
    for ticker in ticker_list:
        data = dm.get_income_statement(ticker)
        data['is_ticker'] = ticker
        data.to_sql('income_statement', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_income_statement():
    connection = sqlite3.connect("graham.db")
    income_statement_data = pd.read_sql("select * from income_statement", connection)
    connection.close()

    return income_statement_data


def get_by_ticker_income_statement(ticker):
    connection = sqlite3.connect("graham.db")
    income_statement_data = pd.read_sql("select * from income_statement where is_ticker = '{}'".format(ticker),
                                        connection)
    connection.close()

    return income_statement_data


def update_balance_sheet():
    print("Updating balance_sheet table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM balance_sheet')
    i = 1
    for ticker in ticker_list:
        data = dm.get_balance_sheet(ticker)
        data['bs_ticker'] = ticker
        data.to_sql('balance_sheet', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_balance_sheet():
    connection = sqlite3.connect("graham.db")
    balance_sheet_data = pd.read_sql("select * from balance_sheet", connection)
    connection.close()

    return balance_sheet_data


def get_by_ticker_balance_sheet(ticker):
    connection = sqlite3.connect("graham.db")
    balance_sheet_data = pd.read_sql("select * from balance_sheet where bs_ticker = '{}'".format(ticker),
                                     connection)
    connection.close()

    return balance_sheet_data


def update_financial_ratios():
    print("Updating financial_ratios table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM financial_ratios')
    i = 1
    for ticker in ticker_list:
        data = dm.get_financial_ratios(ticker)
        data['fr_ticker'] = ticker
        data.to_sql('financial_ratios', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def continue_updating_financial_ratios():
    print("Continuing to update financial_ratios table...")
    df = get_financial_ratios()
    last_ticker = df['fr_ticker'].tolist()[-1]
    ticker_list = get_sp500()['ticker'].tolist()
    ticker_index = ticker_list.index(last_ticker)
    tickers_continuation = ticker_list[ticker_index + 1:]
    connection = sqlite3.connect("graham.db")
    i = ticker_index + 2
    for ticker in tickers_continuation:
        data = dm.get_financial_ratios(ticker)
        data['fr_ticker'] = ticker
        data.to_sql('financial_ratios', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()


def get_financial_ratios():
    connection = sqlite3.connect("graham.db")
    financial_ratios_data = pd.read_sql("select * from financial_ratios", connection)
    connection.close()

    return financial_ratios_data


def get_by_ticker_financial_ratios(ticker):
    connection = sqlite3.connect("graham.db")
    financial_ratios_data = pd.read_sql("select * from financial_ratios where fr_ticker = '{}'".format(ticker),
                                        connection)
    connection.close()

    return financial_ratios_data


# def update_company_financials():
#     print("Updating company_financials table...")
#     connection = sqlite3.connect("graham.db")
#     cursor = connection.cursor()
#     cursor.execute('DELETE FROM company_financials')
#     ticker_list = get_sp500()['ticker'].tolist()
#     i = 1
#     for ticker in ticker_list:
#         data = dw.net_income(ticker).join(dw.stockholders_equity(ticker)).join(dw.shares_outstanding_split_included(ticker))
#         data['eps_calculated'] = data['net_income'] / data['shares_outstanding_split_inc']
#         data['bvps_calculated'] = data['stockholders_equity'] / data['shares_outstanding_split_inc']
#         data['cf_ticker'] = ticker
#         data.to_sql('company_financials', connection, if_exists='append')
#         print("{} {} appended".format(i, ticker))
#         i += 1
#     connection.close()


##########################################################################################
def update_cash_flow_statement():
    print("Updating cash_flow_statement table...")
    ticker_list = get_sp500()['ticker'].tolist()
    connection = sqlite3.connect("graham.db")
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cash_flow_statement')
    i = 1
    for ticker in ticker_list:
        data = dm.get_cash_flow_statement(ticker)
        data['cfs_ticker'] = ticker
        data.to_sql('cash_flow_statement', connection, if_exists='append')
        print("{} {} appended".format(i, ticker))
        i += 1
    connection.close()
############################################################################################
