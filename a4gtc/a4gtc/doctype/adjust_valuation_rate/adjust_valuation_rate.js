// Copyright (c) 2021, Frappé and contributors
// For license information, please see license.txt

frappe.ui.form.on('Adjust Valuation Rate', {
	// refresh: function(frm) {

	// },
	get_valuation_rate: function(frm){
		if(frm.doc.item_code){
			frappe.call({
				method:'a4gtc.a4gtc.doctype.adjust_valuation_rate.adjust_valuation_rate.get_valuation_rate',
				args:{
					item_code:frm.doc.item_code
				},
				callback: function(r){
					if(r.message){
						frm.clear_table("items")
						frm.refresh_fields()
						for (var i in r.message){
							var row = frm.add_child('items')
							row.warehouse = r.message[i][0]
                                                        row.qty = r.message[i][1]
                                                        row.current_valuation_rate = r.message[i][2]
							frm.refresh_fields()
						}
					}
				}
			})
		}
	}
});
