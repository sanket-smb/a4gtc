# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappé and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AdjustValuationRate(Document):
	def on_submit(self):
		doc = frappe.new_doc("Stock Reconciliation")
		doc.purpose = "Stock Reconciliation"
		doc.company = "WRD"
		for i in self.items:
			row = doc.append("items",{})
			row.item_code = self.item_code
			row.warehouse = i.warehouse
			row.qty = i.qty
			row.valuation_rate = i.valuation_rate
		doc.save()
		doc.submit()

@frappe.whitelist()
def get_valuation_rate(item_code):
	ls = frappe.db.sql("""select warehouse, actual_qty, valuation_rate from `tabBin` where item_code=%s and actual_qty > 0 order by actual_qty desc""",item_code,as_list = 1)
	return ls
