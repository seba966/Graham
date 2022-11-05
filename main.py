import download_scrap as ds
import db_connection as db
import download_macrotrends as dm
import pandas as pd
from datetime import date
import condition_check as cc
import yfinance as yf
import time

start_time = time.time()

sp500 = db.get_sp500()
sp500list = sp500['ticker'].tolist()

for el in sp500list:
    cc.company_conditions_check(el)

# print(el, cc.earnings_stability(el)[0])


print("--- %s seconds ---" % (time.time() - start_time))
# print(cc.earnings_stability('AAPL'))

# income_statement_to_update = ['revenue',
#       'cost_of_goods_sold',
#       'gross_profit',
#       'research_and_development_expenses',
#       'sg_a_expenses',
#       'other_operating_income_or_expenses',
#       'operating_expenses',
#       'operating_income',
#       'pretax_income',
#       'income_taxes',
#       'income_after_taxes',
#       'other_income',
#       'income_from_continuous_operations',
#       'income_from_discontinued_operations',
#       'net_income',
#       'ebitda',
#       'ebit',
#       'basic_shares_outstanding',
#       'shares_outstanding']
# balance_sheet_to_update = [
#     'cash_on_hand',
#     'receivables',
#     'inventory',
#     'prepaid_expenses',
#     'other_current_assets',
#     'total_current_assets',
#     'property_plant_and_equipment',
#     'longterm_investments',
#     'goodwill_and_intangible_assets',
#     'other_longterm_assets',
#     'total_longterm_assets',
#     'total_assets',
#     'total_current_liabilities',
#     'long_term_debt',
#     'other_noncurrent_liabilities',
#     'total_long_term_liabilities',
#     'total_liabilities',
#     'common_stock_net',
#     'retained_earnings_accumulated_deficit',
#     'comprehensive_income',
#     'other_share_holders_equity',
#     'share_holder_equity',
#     'total_liabilities_and_share_holders_equity'
# ]
# ee = [
#     'net_income_loss',
#     'total_depreciation_and_amortization_cash_flow',
#     'other_noncash_items',
#     'total_noncash_items',
#     'change_in_accounts_receivable',
#     'change_in_inventories',
#     'change_in_accounts_payable',
#     'change_in_assets_liabilities',
#     'total_change_in_assets_liabilities',
#     'cash_flow_from_operating_activities',
#     'net_change_in_property_plant_and_equipment',
#     'net_change_in_intangible_assets',
#     'net_acquisitions_divestitures',
#     'net_change_in_shortterm_investments',
#     'net_change_in_longterm_investments',
#     'net_change_in_investments_total',
#     'investing_activities_other',
#     'cash_flow_from_investing_activities',
#     'net_longterm_debt',
#     'net_current_debt',
#     'debt_issuance_retirement_net_total',
#     'net_common_equity_issued_repurchased',
#     'net_total_equity_issued_repurchased',
#     'total_common_and_preferred_stock_dividends_paid',
#     'financial_activities_other',
#     'cash_flow_from_financial_activities',
#     'net_cash_flow',
#     'stockbased_compensation',
#     'common_stock_dividends_paid'
# ]
# for el in ee:
#     print('\t{} = {} * 1000000,'.format(el, el))
