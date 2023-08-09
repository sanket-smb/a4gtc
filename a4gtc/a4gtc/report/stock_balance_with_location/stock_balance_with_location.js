// Copyright (c) 2016, vignesh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Balance with Location"] = {
	"filters": [
		{
			"fieldname": "item_group",
			"fieldtype": "Link",
			"label": "Item Group",
			"mandatory": 0,
			"options": "Item Group",
			"wildcard_filter": 0
		},
		{
			"fieldname": "item",
			"fieldtype": "Link",
			"label": "Item",
			"mandatory": 0,
			"options": "Item",
			"wildcard_filter": 0
		}
	]
};

