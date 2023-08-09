from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, datetime
from erpnext.stock.utils import get_latest_stock_qty
import json
from frappe import _, throw, msgprint, utils
from frappe.utils import cint, flt, cstr, comma_or, getdate, add_days, getdate, rounded, date_diff, money_in_words




@frappe.whitelist()
def hellosub(loggedInUser):
	return 'pong'

@frappe.whitelist()
def test():
	return "sucess"

@frappe.whitelist(allow_guest = True)
def get_tyre_item_details():
    #product_name = "testTemplate" #local
    product_name = "A4 TYRES PRODUCT" #client
    master_items_data = frappe.db.sql("""select  item_code,item_name,description,valuation_rate from `tabItem`  where variant_of = %s order by creation desc ;""", (product_name), as_dict=1)
    items_json =[]

    for item_d in master_items_data:
        items_att = {
        "discription":item_d.get("description"),
        "cost":item_d.get("valuation_rate"),
        "total_qty":"",
        "wh_names":"",
        "size":"",
        "year":"",
	"standard_selling_price":0,
        "pcode":item_d.get("item_code"),
        }
        items_att["total_qty"] = get_total_stock_qty_in_all_wh(item_d.get("item_code"))
        items_att["wh_names"] = get_wh_names(item_d.get("item_code"))
        variant_attribute_details = get_variant_attribute_details(item_d.get("item_code"))
        items_att["size"] = variant_attribute_details.get("Size") or ""
        items_att["year"] = variant_attribute_details.get("Year") or ""
        items_att["brand"] = variant_attribute_details.get("Brand") or ""
        items_att["standard_selling_price"] = get_selling_price(item_d.get('item_code')) or 0
        items_json.append(items_att)

    return items_json



@frappe.whitelist()
def get_tyre_item_details_p(page_limit,page_number,item_group):
	#pagination_start
	page_limit=int(page_limit)
	page_number=int(page_number)
	#table_row_count_dic = frappe.db.sql("""select count(*) as count from `tabPacked Box Custom`""",as_dict=1)
	table_row_count_dic = frappe.db.sql("""select count(*) as count from `tabItem` where item_group = %s """,(item_group),as_dict=1)
	table_row_count = table_row_count_dic[0]["count"]
	#new
	table_row_count_float= float(table_row_count)
	page_limit_float = float(page_limit)
	total_page_number_float = table_row_count_float / page_limit_float


	table_row_count_int= int(table_row_count)
	page_limit_int = int(page_limit)

	total_page_number_int =  int(table_row_count_int / page_limit_int)

	if total_page_number_float > total_page_number_int:
		total_page_number_int = total_page_number_int + 1

	total_page_number =  total_page_number_int

	#new
	off_set = (page_number-1 ) * page_limit
	page_limit_conditions= get_page_limit_conditions("creation","asc",page_limit,off_set)
	#pagination_end

	query = """select  item_code,description,item_name,item_group,stock_uom,last_purchase_rate from `tabItem` where item_group = '%s' %s""" % (item_group,page_limit_conditions)
	#print "query",query

	#master_items_data = frappe.db.sql("""select  item_code,item_name,description,valuation_rate from `tabItem`  where variant_of = %s  %s ;""", (product_name,page_limit_conditions), as_dict=1)
	master_items_data = frappe.db.sql(query, as_dict=1)
	items_json =[]
	for item_d in master_items_data:
		items_att = {
		"description":item_d.get("description"),
		"cost":item_d.get("valuation_rate"),
		"total_qty":"",
		"wh_names":"",
		"size":"",
		"year":"",
		"standard_selling_price":0,
		"pcode":item_d.get("item_code"),
		"valuation_rate":"",
		"wh_wise_qty":"",
		"last_purchase_rate":"",
		"last_sold_price":"",
		"stock_in_transit":""

		}
		items_att["total_qty"] = get_total_stock_qty_in_all_wh(item_d.get("item_code"))
		items_att["wh_names"] = get_wh_names(item_d.get("item_code"))
		variant_attribute_details = get_variant_attribute_details(item_d.get("item_code"))
		items_att["size"] = variant_attribute_details.get("Size") or ""
		items_att["year"] = variant_attribute_details.get("Year") or ""
		items_att["brand"] = variant_attribute_details.get("Brand") or ""
		items_att["standard_selling_price"] = get_selling_price(item_d.get('item_code')) or 0
		items_att["VarAt1"] = variant_attribute_details.get("VarAt1")  or ""
		items_att["VarAt2"] = variant_attribute_details.get("VarAt2")  or ""

		#dec22
		items_att["valuation_rate"] = get_valuation_rate(item_d.get("item_code"))
		items_att["wh_wise_qty"] = get_wh_wise_qty_list(item_d.get("item_code"))
		#dec22

		#dec26
		items_att["last_purchase_rate"] = item_d.get("last_purchase_rate")
		si_details = get_si_details(item_d.get("item_code"))
		if si_details :
			items_att["last_sold_price"] = si_details[0]["rate"]
		items_att["stock_in_transit"] = get_stock_in_transit(item_d.get("item_code"))
		#dec26

		items_json.append(items_att)


	#print "items_json",items_json
	item_details = {"cur_page":page_number,"total_count":table_row_count,"total_page":total_page_number,"item_data":items_json}
	return item_details

def get_variant_attribute_details(item_code):
    variant_attribute_dic = frappe.db.sql("""select parent,attribute,attribute_value from `tabItem Variant Attribute` where parent = %s """, (item_code), as_dict=1)
    #print "variant_attribute_dic",variant_attribute_dic
    item_variant_attribute_data={}
    for vad in variant_attribute_dic:
        if vad.get("attribute") == "Size":
            item_variant_attribute_data["Size"] = vad.get("attribute_value")
        if vad.get("attribute") == "Brand":
            item_variant_attribute_data["Brand"] = vad.get("attribute_value")
        if vad.get("attribute") == "Year":
            item_variant_attribute_data["Year"] = vad.get("attribute_value")
        if vad.get("attribute") == "Patten":
            item_variant_attribute_data["Patten"] = vad.get("attribute_value")
        if vad.get("attribute") == "Load_Index":
            item_variant_attribute_data["Load_Index"] = vad.get("attribute_value")
        if vad.get("attribute") == "Speed_Index":
            item_variant_attribute_data["Speed_Index"] = vad.get("attribute_value")
        if vad.get("attribute") == "Series":
            item_variant_attribute_data["Series"] = vad.get("attribute_value")
        if vad.get("attribute") == "Made_In":
            item_variant_attribute_data["Made_In"] = vad.get("attribute_value")
        if vad.get("attribute") == "VarAt1":
            item_variant_attribute_data["VarAt1"] = vad.get("attribute_value")
        if vad.get("attribute") == "VarAt2":
            item_variant_attribute_data["VarAt2"] = vad.get("attribute_value")
    return item_variant_attribute_data

def get_total_stock_qty_in_all_wh(item_code):
    total_stock_qty_in_all_wh = frappe.db.sql("""select sum(actual_qty) as sum_actual_qty from `tabBin` where item_code=%s """, (item_code), as_dict=1)
    return total_stock_qty_in_all_wh[0]["sum_actual_qty"] if  total_stock_qty_in_all_wh else 0

def get_wh_names(item_code):
    total_stock_qty_in_all_wh = frappe.db.sql("""select warehouse from `tabBin` where item_code=%s """, (item_code), as_dict=1)
    wh_list=[]
    for wh_data in total_stock_qty_in_all_wh :
        wh_list.append(wh_data["warehouse"])
    return wh_list

def get_selling_price(item_code):
    selling_price = frappe.db.sql('''select price_list_rate as rate from `tabItem Price` where item_code = %s and price_list = "Standard Selling" and selling = 1 ''',(item_code),as_dict = 1)
    if selling_price:
        return selling_price[0]['rate']
    else:
        return 0


#pagination fun
def get_page_limit_conditions(order_by=None,order_by_type=None,page_limit=None,off_set=None):
    condition = ""
    if order_by:
        condition += " order by "+order_by
    if order_by and order_by_type:
        condition += " "+order_by_type
    if page_limit:
        #print " page_limit",page_limit
        condition += " limit "+str(page_limit)
    condition += " offset "+ str(off_set)
    return condition




#dec22
def get_valuation_rate(item_code):
	val_rate_dic = frappe.db.sql("""select valuation_rate  from `tabBin` where item_code=%s order by creation desc limit 1 """, (item_code), as_dict=1)
	return val_rate_dic[0]["valuation_rate"] if val_rate_dic else 0

def get_wh_wise_qty_list(item_code):
	actual_qty_in_all_wh=[]
	actual_qty_in_all_wh = frappe.db.sql("""select warehouse,actual_qty from `tabBin` where item_code=%s """, (item_code), as_dict=1)
	return actual_qty_in_all_wh
#dec22

#dec26
def get_si_details(item_code):
	details = frappe.db.sql("""select si.name,sii.rate,si.posting_date from `tabSales Invoice` si,`tabSales Invoice Item` sii  where si.name = sii.parent and sii.item_code=%s order by si.creation desc limit 1""", (item_code), as_dict=1)
	return details if details else None

def get_stock_in_transit(item_code):
	ordered_qty_dic = frappe.db.sql("""select sum(ordered_qty) as ordered_qty   from `tabBin` where item_code=%s  """, (item_code), as_dict=1)
	return ordered_qty_dic[0]["ordered_qty"] if ordered_qty_dic else 0
#dec26


"""
a4_tier_local_api
"""

@frappe.whitelist()
def create_stock_entry():
	se_name=None

	try:
		reqData = json.loads(frappe.request.data)
		se_entity = reqData
		#print "reqData from create_stock_entry",reqData
		se = frappe.new_doc("Stock Entry")
		#se.purpose = se_entity.get("action")
		se.stock_entry_type = se_entity.get("action")
		#se.company = "Epoch Consulting"
		se.company = "WRD"
		#se.company = "Epoch Consulting"

		se.set('items', [])
		for item in se_entity.get("items_list") :
			se_item = se.append('items', {})
			se_item.item_code = item["item_code"]
			se_item.qty = item["qty"]
			#se_item.serial_no = item["serial_num"]
			se_item.uom =  item["uom"]
			se_item.conversion_factor = 1
			se_item.stock_uom =  item["uom"]
			se_item.cost_center="Main - WRD"

			if se_entity.get("action") == "Material Transfer":
				se_item.s_warehouse =  item["s_wh"]
				se_item.t_warehouse =  item["t_wh"]
			if se_entity.get("action") == "Material Issue":
				se_item.s_warehouse =  item["s_wh"]
			if se_entity.get("action") == "Material Receipt":
				se_item.t_warehouse =  item["t_wh"]

		se.save(ignore_permissions=True)
		se.submit()
		frappe.db.commit()
		se_name = se.name
	except Exception as e:
		#print "sur_Exception from create_stock_entry",e,"traceback:", frappe.get_traceback()
		pass
	finally:
		return se_name
#dec27

@frappe.whitelist()
def create_stock_entry_test():
	reqData = json.loads(frappe.request.data)
	se_entity = reqData
	se = frappe.new_doc("Stock Entry")
	#se.purpose = se_entity.get("action")
	#se.company = "Epoch Consulting"
	se.company = "WRD"
	se.stock_entry_type = se_entity.get("action")
	#se.purpose = se_entity.get("action")

	se.set('items', [])
	for item in se_entity.get("items_list") :
		se_item = se.append('items', {})
		se_item.item_code = item["item_code"]
		se_item.qty = item["qty"]
		se_item.uom = item["uom"]
		se_item.conversion_factor = 1
		se_item.stock_uom = "Nos"
		se_item.cost_center="Main - WRD"
		if se_entity.get("action") == "Material Transfer":
			se_item.s_warehouse =  item["s_wh"]
			se_item.t_warehouse =  item["t_wh"]
		if se_entity.get("action") == "Material Issue":
			se_item.s_warehouse =  item["s_wh"]
		if se_entity.get("action") == "Material Receipt":
			se_item.t_warehouse =  item["t_wh"]

	se.save(ignore_permissions=True)
	se.submit()
	frappe.db.commit()
	return se.name

@frappe.whitelist()
def test_input_data():
	reqData = json.loads(frappe.request.data)
	return reqData

