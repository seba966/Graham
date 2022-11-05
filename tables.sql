CREATE TABLE sp500 (
	ticker text PRIMARY KEY,
	cik text
);

CREATE TABLE company_financials (
	 cf_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 net_income REAL,
	 stockholders_equity REAL,
	 shares_outstanding_split_inc INTEGER,
	 eps_calculated REAL,
	 bvps_calculated REAL,
	 cf_ticker TEXT,
	 FOREIGN KEY (cf_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE company_info (
	 ci_id INTEGER PRIMARY KEY,
	 market_cap REAL,
	 current_assets REAL,
	 current_liability REAL,
	 long_term_debt REAL,
	 ci_ticker TEXT, 
	 FOREIGN KEY (ci_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE annual_share_return (
	 asr_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 annual_return INTEGER,
	 asr_ticker TEXT,
	 FOREIGN KEY (asr_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE dividends_paid (
	 d_id INTEGER PRIMARY KEY,
	 date TEXT,
	 dividend INTEGER,
	 d_ticker TEXT,
	 FOREIGN KEY (d_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE stock_split (
	 s_id INTEGER PRIMARY KEY,
	 date TEXT,
	 dividend INTEGER,
	 s_ticker TEXT,
	 FOREIGN KEY (s_ticker) REFERENCES sp500 (ticker)
);


CREATE TABLE income_statement (
	 is_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 revenue REAL,
	 cost_of_goods_sold REAL,
	 gross_profit REAL,
	 research_and_development_expenses REAL,
	 sg_a_expenses REAL,
	 other_operating_income_or_expenses REAL,
	 operating_expenses REAL,
	 operating_income REAL,
	 total_nonoperating_income_expense REAL,
	 pretax_income REAL,
	 income_taxes REAL,
	 income_after_taxes REAL,
	 other_income REAL,
	 income_from_continuous_operations REAL,
	 income_from_discontinued_operations REAL,
	 net_income REAL,
	 ebitda REAL,
	 ebit REAL,
	 basic_shares_outstanding REAL,
	 shares_outstanding REAL,
	 basic_eps REAL,
	 diluted_eps REAL,
	 is_ticker TEXT,
	 FOREIGN KEY (is_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE balance_sheet (
	 bs_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 cash_on_hand REAL,
	 receivables REAL,
	 inventory REAL,
	 prepaid_expenses REAL,
	 other_current_assets REAL,
	 total_current_assets REAL,
	 property_plant_and_equipment REAL,
	 longterm_investments REAL,
	 goodwill_and_intangible_assets REAL,
	 other_longterm_assets REAL,
	 total_longterm_assets REAL,
	 total_assets REAL,
	 total_current_liabilities REAL,
	 long_term_debt REAL,
	 other_noncurrent_liabilities REAL,
	 total_long_term_liabilities REAL,
	 total_liabilities REAL,
	 common_stock_net REAL,
	 retained_earnings_accumulated_deficit REAL,
	 comprehensive_income REAL,
	 other_share_holders_equity REAL,
	 share_holder_equity REAL,
	 total_liabilities_and_share_holders_equity REAL,
	 bs_ticker TEXT,
	 FOREIGN KEY (bs_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE cash_flow_statement (
	 cfs_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 net_income_loss REAL,
	 total_depreciation_and_amortization_cash_flow REAL,
	 other_noncash_items REAL,
	 total_noncash_items REAL,
	 change_in_accounts_receivable REAL,
	 change_in_inventories REAL,
	 change_in_accounts_payable REAL,
	 change_in_assets_liabilities REAL,
	 total_change_in_assets_liabilities REAL,
	 cash_flow_from_operating_activities REAL,
	 net_change_in_property_plant,_and_equipment REAL,
	 net_change_in_intangible_assets REAL,
	 net_acquisitions_divestitures REAL,
	 net_change_in_shortterm_investments REAL,
	 net_change_in_longterm_investments REAL,
	 net_change_in_investments_total REAL,
	 investing_activities_other REAL,
	 cash_flow_from_investing_activities REAL,
	 net_longterm_debt REAL,
	 net_current_debt REAL,
	 debt_issuance_retirement_net_total REAL,
	 net_common_equity_issued_repurchased REAL,
	 net_total_equity_issued_repurchased REAL,
	 total_common_and_preferred_stock_dividends_paid REAL,
	 financial_activities_other REAL,
	 cash_flow_from_financial_activities REAL,
	 net_cash_flow REAL,
	 stockbased_compensation REAL,
	 common_stock_dividends_paid REAL,
	 cfs_ticker TEXT,
	 FOREIGN KEY (cfs_ticker) REFERENCES sp500 (ticker)
);

CREATE TABLE financial_ratios (
	 fr_id INTEGER PRIMARY KEY,
	 year INTEGER,
	 current_ratio REAL,
	 longterm_debt_capital REAL,
	 debt_equity_ratio REAL,
	 gross_margin REAL,
	 operating_margin REAL,
	 ebit_margin REAL,
	 ebitda_margin REAL,
	 pretax_profit_margin REAL,
	 net_profit_margin REAL,
	 asset_turnover REAL,
	 inventory_turnover_ratio REAL,
	 receiveable_turnover REAL,
	 days_sales_in_receivables REAL,
	 roe_return_on_equity REAL,
	 return_on_tangible_equity REAL,
	 roa_return_on_assets REAL,
	 roi_return_on_investment REAL,
	 book_value_per_share REAL,
	 operating_cash_flow_per_share REAL,
	 free_cash_flow_per_share REAL,
	 fr_ticker TEXT,
	 FOREIGN KEY (fr_ticker) REFERENCES sp500 (ticker)
);

CREATE INDEX is_ticker_index ON income_statement (
	is_ticker
)

CREATE INDEX bs_ticker_index ON balance_sheet (
	bs_ticker
)

CREATE INDEX cfs_ticker_index ON cash_flow_statement (
	cfs_ticker
)

CREATE INDEX fr_ticker_index ON financial_ratios (
	fr_ticker
)
