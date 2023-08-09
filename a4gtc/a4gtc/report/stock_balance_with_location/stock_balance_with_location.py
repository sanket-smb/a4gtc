# Copyright (c) 2013, Aerele Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.db_query import DatabaseQuery

def execute(filters=None):
	columns = [
		{
		"fieldname": "item_code",
		"fieldtype": "Link",
		"label": "Item",
		"options": "Item",
		"width": 100
		},
		{
		"fieldname": "brand",
		"fieldtype": "Data",
		"label": "Brand",
		"width": 75
		},
		{
		"fieldname": "description",
		"fieldtype": "Data",
		"label": "Description",
		"width": 100
		},
		{
		"fieldname": '13 - KABAD STORE - WRD',
		"fieldtype": "Data",
		"label": '13 - KABAD STORE - WRD',
		"width": 60
		},
		{
                "fieldname": '12 - Fahaheel Branch - WRD',
                "fieldtype": "Data",
                "label": '12 - Fahaheel Branch - WRD',
                "width": 60
                },

		{
                "fieldname": "11 - GARAGE SHIFA - WRD",
                "fieldtype": "Data",
                "label": "11 - GARAGE SHIFA - WRD",
                "width": 60
                },
		{
                "fieldname": "10-WH1 - WRD",
                "fieldtype": "Data",
                "label": "10-WH1 - WRD",
                "width": 60
                },
		{
		"fieldname": "09 - SAMARA - WRD",
		"fieldtype": "Data",
		"label": "09 - SAMARA - WRD",
		"width": 60
		},
		{
		"fieldname": "08 - AL FAJER - WRD",
		"fieldtype": "Data",
		"label": "08 - AL FAJER - WRD",
		"width": 60
		},
		{
		"fieldname": "07 - DIMAH - WRD",
		"fieldtype": "Data",
		"label": "07 - DIMAH - WRD",
		"width": 60
		},
		{
		"fieldname": "06 - JAHARA 1 - WRD",
		"fieldtype": "Data",
		"label": "06 - JAHARA 1 - WRD",
		"width": 60
		},
		{
		"fieldname": "05 - BAREEM - WRD",
		"fieldtype": "Data",
		"label": "05 - BAREEM - WRD",
		"width": 60
		},
		{
		"fieldname": "04 - AL MAILEM LC6 - WRD",
		"fieldtype": "Data",
		"label": "04 - AL MAILEM LC6 - WRD",
		"width": 60
		},
		{
		"fieldname": "03 - AUTOMALL - WRD",
		"fieldtype": "Data",
		"label": "03 - AUTOMALL - WRD",
		"width": 60
		},
		{
		"fieldname": "02 - FAHAD - WRD",
		"fieldtype": "Data",
		"label": "02 - FAHAD - WRD",
		"width": 60
		},
		{
		"fieldname": "01 - FATAYER - WRD",
		"fieldtype": "Data",
		"label": "01 - FATAYER - WRD",
		"width": 60
		},
		{
		"fieldname": "Stores - WRD",
		"fieldtype": "Data",
		"label": "Stores - WRD",
		"width": 60
		},
		{
		"fieldname": "Total Quantity - WRD",
		"fieldtype": "Data",
		"label": "Total Quantity - WRD",
		"width": 60
		},
		{
                "fieldname": "Valuation Rate - WRD",
                "fieldtype": "Data",
                "label": "Valuation Rate - WRD",
                "width": 60
                },
		{
		"fieldname": "Total Value - WRD",
		"fieldtype": "Data",
		"label": "Total Value - WRD",
		"width": 60
		},
		{
		"fieldname": "Main Stores-Import - Import",
		"fieldtype": "Data",
		"label": "Main Stores-Import - Import",
		"width": 60
		},
		{
		"fieldname": "Jahra Store - Import",
		"fieldtype": "Data",
		"label": "Jahra Store - Import",
		"width": 60
		},
		{
		"fieldname": "Fahaheel Store - Import",
		"fieldtype": "Data",
		"label": "Fahaheel Store - Import",
		"width": 60
		},
		{
                "fieldname": "AMGHARA MAIN Store - Import",
                "fieldtype": "Data",
                "label": "AMGHARA MAIN Store - Import",
                "width": 60
                },
		{
		"fieldname": "Shuwaikh Store - Import",
		"fieldtype": "Data",
		"label": "Shuwaikh Store - Import",
		"width": 60
		},
		{
		"fieldname": "Total Quantity - Import",
		"fieldtype": "Data",
		"label": "Total Quantity - Import",
		"width": 60
		},
		{
                "fieldname": "Valuation Rate - Import",
                "fieldtype": "Data",
                "label": "Valuation Rate - Import",
                "width": 60
		},
		{
		"fieldname": "Total Value - Import",
		"fieldtype": "Data",
		"label": "Total Value - Import",
		"width": 60
		},
		{
		"fieldname": "Final Quantity",
		"fieldtype": "Data",
		"label": "Final Quantity",
		"width": 60
		},
		{
		"fieldname": "Final Value",
		"fieldtype": "Data",
		"label": "Final Value",
		"width": 60
		},
	]
	data = get_reportdata(filters)
	return columns, data

def get_reportdata(filters=None):
	item_detail= {}
	item_group = None
	item = None
	if 'item_group' in filters:
		item_group = filters['item_group']
	
	if 'item' in filters:
		item = filters['item']

	location_wrd = ['11 - GARAGE SHIFA - WRD','10-WH1 - WRD','09 - SAMARA - WRD', '08 - AL FAJER - WRD', '07 - DIMAH - WRD', '06 - JAHARA 1 - WRD',
	'05 - BAREEM - WRD', '04 - AL MAILEM LC6 - WRD', '03 - AUTOMALL - WRD', '02 - FAHAD - WRD', '01 - FATAYER - WRD',
	'Stores - WRD','12 - Fahaheel Branch - WRD','13 - KABAD STORE - WRD']
	location_import = ['Main Stores-Import - Import', 'Jahra Store - Import', 'Fahaheel Store - Import',
	'Shuwaikh Store - Import', 'AMGHARA MAIN Store - Import']
	details = get_data(item_group=item_group, item_code=item)
	for detail in details:
		item_detail[detail['item_code']] = {'item_code': detail['item_code'], 'Total Quantity - WRD': 0,
		'Valuation Rate - WRD':0, 'Total Value - WRD': 0, 'Total Quantity - Import': 0, 'Valuation Rate - Import':0, 'Total Value - Import': 0,
		'Final Quantity': 0, 'Final Value': 0}
	for detail in details:
		item_detail[detail['item_code']][detail['warehouse']] = detail['actual_qty']
		item_detail[detail['item_code']]['name'] = detail['item_name']
		item_detail[detail['item_code']]['brand'] = detail['brand']
		item_detail[detail['item_code']]['description'] = detail['description']
		if detail['warehouse'] in location_wrd:
			item_detail[detail['item_code']]['Total Quantity - WRD'] += detail['actual_qty']
			item_detail[detail['item_code']]['Total Value - WRD'] += detail['stock_value']

			item_detail[detail['item_code']]['Final Quantity'] += detail['actual_qty']
			item_detail[detail['item_code']]['Final Value'] += detail['stock_value']

			item_detail[detail['item_code']]['Total Quantity - WRD'] = round(item_detail[detail['item_code']]['Total Quantity - WRD'], 3)
			item_detail[detail['item_code']]['Total Value - WRD'] = round(item_detail[detail['item_code']]['Total Value - WRD'], 3)
			item_detail[detail['item_code']]['Final Quantity'] = round(item_detail[detail['item_code']]['Final Quantity'], 3)
			item_detail[detail['item_code']]['Final Value'] = round(item_detail[detail['item_code']]['Final Value'], 3)
		elif detail['warehouse'] in location_import:
			item_detail[detail['item_code']]['Total Quantity - Import'] += detail['actual_qty']
			item_detail[detail['item_code']]['Total Value - Import'] += detail['stock_value']

			item_detail[detail['item_code']]['Final Quantity'] += detail['actual_qty'] 
			item_detail[detail['item_code']]['Final Value'] += detail['stock_value']

			item_detail[detail['item_code']]['Total Quantity - Import'] = round(item_detail[detail['item_code']]['Total Quantity - Import'], 3)
			item_detail[detail['item_code']]['Total Value - Import'] = round(item_detail[detail['item_code']]['Total Value - Import'], 3)
			item_detail[detail['item_code']]['Final Quantity'] = round(item_detail[detail['item_code']]['Final Quantity'], 3)
			item_detail[detail['item_code']]['Final Value'] = round(item_detail[detail['item_code']]['Final Value'], 3)
		item_detail[detail['item_code']]['warehouse'] = detail['warehouse']
		if item_detail[detail['item_code']]['Total Quantity - WRD'] and  item_detail[detail['item_code']]['Total Value - WRD']:
			item_detail[detail['item_code']]['Valuation Rate - WRD'] = round(item_detail[detail['item_code']]['Total Value - WRD']/item_detail[detail['item_code']]['Total Quantity - WRD'], 3)
		if  item_detail[detail['item_code']]['Total Quantity - Import'] and item_detail[detail['item_code']]['Total Value - Import']:
			item_detail[detail['item_code']]['Valuation Rate - Import'] = round(item_detail[detail['item_code']]['Total Value - Import']/item_detail[detail['item_code']]['Total Quantity - Import'], 3)
	return [i for i in item_detail.values() if i['Final Value']]
	#return [*item_detail.values()]
def get_data(item_code=None, warehouse=None, item_group=None,
	start=0, sort_by='actual_qty', sort_order='desc'):
	'''Return data to render the item dashboard'''
	filters = []
	if item_code:
		filters.append(['item_code', '=', item_code])
	if warehouse:
		filters.append(['warehouse', 'in', warehouse])
	if item_group:
		lft, rgt = frappe.db.get_value("Item Group", item_group, ["lft", "rgt"])
		items = frappe.db.sql_list("""
			select i.name from `tabItem` i
			where exists(select name from `tabItem Group`
				where name=i.item_group and lft >=%s and rgt<=%s)
		""", (lft, rgt))

		filters.append(['item_code', 'in', items])
	try:
		# check if user has any restrictions based on user permissions on warehouse
		if DatabaseQuery('Warehouse', user=frappe.session.user).build_match_conditions():
			filters.append(['warehouse', 'in', [w.name for w in frappe.get_list('Warehouse')]])
	except frappe.PermissionError:
		# user does not have access on warehouse
		return []

	items = frappe.db.get_all('Bin', fields=['item_code', 'warehouse', 'projected_qty',
			'reserved_qty', 'reserved_qty_for_production', 'reserved_qty_for_sub_contract', 'actual_qty', 'valuation_rate', 'stock_value'],
		filters=filters,
		order_by=sort_by + ' ' + sort_order,
		limit_start=start)

	for item in items:
		item.update({
			'item_name': frappe.get_cached_value("Item", item.item_code, 'item_name'),
			'description': frappe.get_cached_value("Item", item.item_code, 'description'),
			'standard_rate': frappe.get_cached_value("Item", item.item_code, 'standard_rate'),
			'brand': frappe.get_cached_value("Item", item.item_code, 'brand'),
			'disable_quick_entry': frappe.get_cached_value("Item", item.item_code, 'has_batch_no')
				or frappe.get_cached_value("Item", item.item_code, 'has_serial_no'),
		})

	return items

