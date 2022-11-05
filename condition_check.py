import db_connection as db
import pandas as pd
from datetime import datetime, date


def company_conditions_check(ticker):
    one = adequate_size(ticker)[0]
    two = strong_financial_condition(ticker)[0]
    three = earnings_stability(ticker)[0]
    four = dividend_record(ticker)[0]
    five = earnings_growth(ticker)[0]
    six = moderate_pe_ratio(ticker)[0]
    seven = moderate_price_to_book_ratio(ticker)[0]
    eight = steel_condition(ticker)[0]
    print(ticker, one, two, three, four, five, six, seven, eight)


def adequate_size(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company has market cap higher or equal 2 bilion (miliard),\n
    market cap value of company,\n
    do the company has enterprise higher or equal 2 bilion (miliard),\n
    enterprise value of company\n
    )
    """
    company_info = db.get_by_ticker_company_info(ticker)
    market_cap = company_info['market_cap'].tolist()[0]
    enterprise_value = company_info['enterprise_value'].tolist()[0]
    market_cap_size_condition = True if market_cap >= 2000000000 else False
    enterprise_value_size_condition = True if enterprise_value >= 2000000000 else False

    return market_cap_size_condition, market_cap, enterprise_value_size_condition, enterprise_value


def strong_financial_condition(ticker):
    """
    returns the tuple with information of\n
    (\n
    do both below conditions are met,\n
    do the company has current_assets / current_liabilities >= 2,\n
    do the company has (current_assets - current_liabilities) / long_term_debt >= 1,\n
    do the long term debt is from annual report (previous year),\n
    do the long term debt is equal zero\n
    )
    """
    company_info = db.get_by_ticker_company_info(ticker)
    current_assets = company_info['current_assets'].tolist()[0]
    current_liabilities = company_info['current_liabilities'].tolist()[0]
    long_term_debt = company_info['long_term_debt'].tolist()[0]
    # print(long_term_debt)
    is_long_term_debt_equal_zero = False
    is_long_term_debt_from_annual_report = False

    first_condition = True if current_assets / current_liabilities >= 2 else False
    if long_term_debt is None:
        balance_sheet = db.get_by_ticker_balance_sheet(ticker)
        long_term_debt = balance_sheet['long_term_debt'].tolist()[-1]
        is_long_term_debt_from_annual_report = True
        if long_term_debt is None:
            long_term_debt = 1
            is_long_term_debt_from_annual_report = False
            is_long_term_debt_equal_zero = True
    second_condition = True if (current_assets - current_liabilities) / long_term_debt >= 1 else False
    both_conditions = True if (first_condition == True and second_condition == True) else False

    return both_conditions, first_condition, second_condition, is_long_term_debt_from_annual_report, \
        is_long_term_debt_equal_zero


def earnings_stability(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company has positive annual share return for last 10 years,\n
    dataframe with positive years,\n
    dataframe with negative years\n
    )
    """
    annual_share_return = db.get_by_ticker_annual_share_return(ticker)
    annual_share_return_last10y = annual_share_return.tail(10)
    gain_years = []
    gain_values = []
    loss_years = []
    loss_values = []
    for index, row in annual_share_return_last10y.iterrows():
        if row['annual_return'] > 0:
            gain_years.append(row['year'])
            gain_values.append(row['annual_return'])
        else:
            loss_years.append(row['year'])
            loss_values.append(row['annual_return'])
    gain_df = pd.Series(data=gain_values, index=gain_years, name='gain_years')
    loss_df = pd.Series(data=loss_values, index=loss_years, name='loss_years')
    full_gain_condition = True if len(gain_df) == 10 else False

    return full_gain_condition, gain_df, loss_df


def dividend_record(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company paid dividend at least 4 times per year in last 20 years,\n
    how many times in the last 20 years the company paid dividend at lest 4 times,\n
    do the company skipped to pay dividend in last 20 years,\n
    how many times in the last 20 years the company skipped to pay dividend,\n
    do the company never paid dividend in last 20 years,\n
    dataframe with dividends paid per year\n
    )
    """
    dividends_paid = db.get_by_ticker_dividends_paid(ticker)
    dividends_paid['date'] = pd.to_datetime(dividends_paid["date"])
    dividends_paid_last20y = dividends_paid.loc[dividends_paid['date'] > datetime(2002, 1, 1)]
    current_year = datetime.today().year
    last20y = [current_year - i for i in range(21)]
    last20y.reverse()
    dividends_paid_in_year_number_list = []
    dividends_paid_in_year_sum_list = []
    iteration_list = list(dividends_paid_last20y.iterrows())
    zeros_number = 0
    at_least_4_number = 0
    for year in last20y:
        i = 0
        dividends_paid_in_year_number = 0
        dividends_paid_in_year_sum = 0
        for index, row in iteration_list[i:]:
            if row['date'].year == year:
                dividends_paid_in_year_number += 1
                dividends_paid_in_year_sum += row['dividend']
                i += 1
        if dividends_paid_in_year_number == 0:
            zeros_number += 1
        elif dividends_paid_in_year_number >= 4:
            at_least_4_number += 1
        dividends_paid_in_year_number_list.append(dividends_paid_in_year_number)
        dividends_paid_in_year_sum_list.append(dividends_paid_in_year_sum)
    df = pd.DataFrame(data={'number_of_dividends': dividends_paid_in_year_number_list,
                            'dividends_paid_sum': dividends_paid_in_year_sum_list},
                      index=pd.Series(last20y, name='year', dtype='Int64'))

    dividends_paid_in_last20y_condition = True if zeros_number == 0 else False
    dividends_paid_at_least_4_times_in_last20y_condition = True if at_least_4_number >= 20 else False
    dividends_never_paid_in_last20y_condition = True if zeros_number == 21 else False

    return dividends_paid_at_least_4_times_in_last20y_condition, at_least_4_number, \
        dividends_paid_in_last20y_condition, zeros_number, dividends_never_paid_in_last20y_condition, df


def earnings_growth(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company meets condition avarage eps from last 3 years / avarage eps of first three years in last 10 years
    is higher or equal 1,33,\n
    avarage of last 3 years,\n
    avarage of first 3 ytears\n
    )\n
    (eps current_year - 1 + eps current_year - 2 + eps current_year - 3)/3 / \n
    (eps current_year - 9 + eps current_year - 10 + eps current_year - 11)/3 >= 1,33
    """
    income_statement = db.get_by_ticker_income_statement(ticker)
    diluted_eps = income_statement[['year', 'diluted_eps']]
    current_year = datetime.today().year
    try:
        cy_min_1 = diluted_eps.loc[diluted_eps['year'] == current_year - 1]['diluted_eps'].values[0]
        cy_min_2 = diluted_eps.loc[diluted_eps['year'] == current_year - 2]['diluted_eps'].values[0]
        cy_min_3 = diluted_eps.loc[diluted_eps['year'] == current_year - 3]['diluted_eps'].values[0]
        cy_min_9 = diluted_eps.loc[diluted_eps['year'] == current_year - 9]['diluted_eps'].values[0]
        cy_min_10 = diluted_eps.loc[diluted_eps['year'] == current_year - 10]['diluted_eps'].values[0]
        cy_min_11 = diluted_eps.loc[diluted_eps['year'] == current_year - 11]['diluted_eps'].values[0]
        last_3y_avg = (cy_min_1 + cy_min_2 + cy_min_3) / 3
        first_3y_avg = (cy_min_9 + cy_min_10 + cy_min_11) / 3
        earnings_growth_condition = True if last_3y_avg / first_3y_avg >= 1.33 else False
    except IndexError:
        earnings_growth_condition = False
        last_3y_avg = None
        first_3y_avg = None

    return earnings_growth_condition, last_3y_avg, first_3y_avg


def moderate_pe_ratio(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company meets condition that the PE ratio is lower or equal 15,\n
    the PE ratio value of the company\n
    )
    """
    income_statement = db.get_by_ticker_income_statement(ticker)
    diluted_eps = income_statement[['year', 'diluted_eps']]
    current_year = datetime.today().year
    company_info = db.get_by_ticker_company_info(ticker)
    try:
        cy_min_1 = diluted_eps.loc[diluted_eps['year'] == current_year - 1]['diluted_eps'].values[0]
        cy_min_2 = diluted_eps.loc[diluted_eps['year'] == current_year - 2]['diluted_eps'].values[0]
        cy_min_3 = diluted_eps.loc[diluted_eps['year'] == current_year - 3]['diluted_eps'].values[0]
        last_3y_avg = (cy_min_1 + cy_min_2 + cy_min_3) / 3
        current_price = company_info['current_price'].values[0]
        pe = current_price / last_3y_avg
        moderate_pe_ratio_condition = True if pe <= 15 else False
    except IndexError:
        moderate_pe_ratio_condition = False
        pe = None

    return moderate_pe_ratio_condition, pe


def moderate_price_to_book_ratio(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company meets condition that the PTB ratio is lower or equal 1,5,\n
    the PTB ratio value of the company\n
    )
    """
    financial_ratios = db.get_by_ticker_financial_ratios(ticker)
    company_info = db.get_by_ticker_company_info(ticker)
    try:
        book_value_per_share = financial_ratios[['book_value_per_share']].values[-1]
        current_price = company_info['current_price'].values[0]
        ptb = float(current_price / book_value_per_share)
        moderate_ptb_condition = True if ptb <= 1.5 else False
    except (IndexError, TypeError):
        moderate_ptb_condition = False
        ptb = None

    return moderate_ptb_condition, ptb


def steel_condition(ticker):
    """
    returns the tuple with information of\n
    (\n
    do the company meets steel condition that pe * ptb <= 22,5,\n
    pe * ptb value\n
    )
    """
    pe = moderate_pe_ratio(ticker)[1]
    ptb = moderate_price_to_book_ratio(ticker)[1]
    try:
        result = pe * ptb
        steel_condition_check = True if result <= 22.5 else False
    except (IndexError, TypeError):
        steel_condition_check = False
        result = None

    return steel_condition_check, result
