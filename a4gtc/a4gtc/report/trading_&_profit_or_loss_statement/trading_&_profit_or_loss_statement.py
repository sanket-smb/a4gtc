# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from erpnext.accounts.report.financial_statements import (get_period_list, get_columns, get_data)



def get_sum_data(data):
	acc = data[0]['account']
	sum = 0
	for i in data[1:]:
		if len(i) and ('parent_account' in  list(i.keys()) and i['parent_account'] == acc) or ( 'indent' in list(i.keys()) and int(i['indent']) == 0 ):
			if i['total']:
				sum += float(i['total'])
	k = list(data[0].keys())
	data[0]['total'] = '%.3f'%sum
	for i in k:
		if '_' in i and i.split('_')[0].isalpha() and i.split('_')[1].isnumeric():
			data[0][i] = '%.3f'%sum
	return data

def execute(filters=None):
	if not filters:return []
	if filters.filter_based_on == 'Date Range' and (filters.period_start_date == None or filters.period_end_date == None):
		return []
	period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.periodicity, filters.period_start_date, filters.period_end_date,
		filters.accumulated_values, filters.company, filter_based_on=filters.filter_based_on)
	total_revenue = []
	cost_of_sales = []
	other_income = []
	operating_cost = []
	income = get_data(filters.company, "Income", "Credit", period_list, filters = filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	expense = get_data(filters.company, "Expense", "Debit", period_list, filters=filters,
		accumulated_values=filters.accumulated_values,
		ignore_closing_entries=True, ignore_accumulated_values_for_fy= True)

	if not len(income) and not len(expense):
		frappe.msgprint("No data available for the period")
		return []
		
	i = 0
	for d in income:
		if len(d) and 'account' in list(d.keys()) and 'Total Other Income' in d['account']:
			i = 1
		if "Income" in d or 'Expences' in d:continue
		if not i:
			total_revenue.append(d)
		else:
			if len(d) and 'indent' in list(d.keys()):
				d.indent = int(d.indent) - 1
			other_income.append(d)


	i = 0
	for d in expense:
		if len(d) and 'account' in list(d.keys()) and 'Total Operating Costs' in d['account']:
			i = 1
		if not i:
			cost_of_sales.append(d)
		else:
			operating_cost.append(d)
	net_profit_loss = get_net_profit_loss(income, expense, period_list, filters.company, filters.presentation_currency)
	new_data = []
	if len(other_income):
		other_income[0].parent_account = ''
		other_income = get_sum_data(other_income[:-2])
	if len(total_revenue):
		total_revenue = get_sum_data(total_revenue)
		k = list(total_revenue[0].keys())
		var = ''
		for i in k:
			if '_' in i and i.split('_')[0].isalpha() and i.split('_')[1].isnumeric():
				var = i

	if len(cost_of_sales):
		cost_of_sales = get_sum_data(cost_of_sales)
	if len(operating_cost):
		operating_cost = get_sum_data(operating_cost[:-2])

	tot_rev = 0
	if len(total_revenue):
		tot_rev = float(total_revenue[0]['total'])

	cost_sale = 0
	if len(cost_of_sales):
		cost_sale = float(cost_of_sales[0]['total'])

	oincome = 0
	if len(other_income):
		oincome = float(other_income[0]['total'])

	op_cost = 0
	if len(operating_cost):
		op_cost = float(operating_cost[0]['total'])


	direct_profit =  '%.3f'%(tot_rev - cost_sale)
	net_profit = '%.3f'%(float(direct_profit) + oincome - op_cost)

	new_data.extend(total_revenue or [])
	new_data.extend(cost_of_sales or [])
	new_data.append({})
	new_data.append({'account': 'Direct Profit',
					'parent_account': '',
					'indent': 0.0,
					'year_start_date': '2021-04-01',
					'year_end_date': '2022-03-31',
					'currency': 'KWD',
					'include_in_gross': 0,
					'account_type': '',
					'is_group': 0,
					'opening_balance': -0.0,
					'account_name': 'Direct Profit',
					var: direct_profit,
					'has_value': True,
					'total': direct_profit
		
	})
	new_data.append({})
	new_data.extend(other_income or [])
	new_data.extend(operating_cost or [])
	new_data.append({})
	new_data.append({'account': 'Net Profit',
					'parent_account': '',
					'indent': 0.0,
					'year_start_date': '2021-04-01',
					'year_end_date': '2022-03-31',
					'currency': 'KWD',
					'include_in_gross': 0,
					'account_type': '',
					'is_group': 0,
					'opening_balance': -0.0,
					'account_name': 'Net Profit',
					var: net_profit,
					'has_value': True,
					'total': net_profit
		
	})
	new_data.append({})
	columns = get_columns(filters.periodicity, period_list, filters.accumulated_values, filters.company)

	chart = get_chart_data(filters, columns, income, expense, net_profit_loss)

	return columns, new_data

def get_net_profit_loss(income, expense, period_list, company, currency=None, consolidated=False):
	total = 0
	net_profit_loss = {
		"account_name": "'" + _("Profit for the year") + "'",
		"account": "'" + _("Profit for the year") + "'",
		"warn_if_negative": True,
		"currency": currency or frappe.get_cached_value('Company',  company,  "default_currency")
	}

	has_value = False

	for period in period_list:
		key = period if consolidated else period.key
		total_income = flt(income[-2][key], 3) if income else 0
		total_expense = flt(expense[-2][key], 3) if expense else 0

		net_profit_loss[key] = total_income - total_expense

		if net_profit_loss[key]:
			has_value=True

		total += flt(net_profit_loss[key])
		net_profit_loss["total"] = total

	if has_value:
		return net_profit_loss

def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[2:]]

	income_data, expense_data, net_profit = [], [], []

	for p in columns[2:]:
		if income:
			income_data.append(income[-2].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[-2].get(p.get("fieldname")))
		if net_profit_loss:
			net_profit.append(net_profit_loss.get(p.get("fieldname")))

	datasets = []
	if income_data:
		datasets.append({'name': _('Income'), 'values': income_data})
	if expense_data:
		datasets.append({'name': _('Expense'), 'values': expense_data})
	if net_profit:
		datasets.append({'name': _('Net Profit/Loss'), 'values': net_profit})

	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}

	if not filters.accumulated_values:
		chart["type"] = "bar"
	else:
		chart["type"] = "line"

	chart["fieldtype"] = "Currency"

	return chart

