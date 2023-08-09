// Copyright (c) 2016, Frappé and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Trading & Profit or Loss Statement"] = $.extend({},
		erpnext.financial_statements);

	erpnext.utils.add_dimensions('Trading & Profit or Loss Statement', 10);

	frappe.query_reports["Trading & Profit or Loss Statement"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "period_start_date",
			"label": __("Period Start Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "period_end_date",
			"label": __("Period End Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "filter_based_on",
			"label": __("Based on"),
			"fieldtype": "Select",
			"options": ['Fiscal Year', 'Date Range'],
			"default": 'Fiscal Year'
		},
		{
			"fieldname": "accumulated_values",
			"label": __("Accumulated Values"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});

