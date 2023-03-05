# Copyright (c) 2023, libracore and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	conditions = get_condition(filters)
	print("Conditions: {0}".format(conditions))
	data_sql = frappe.db.sql(
		"""SELECT
			`tabSales Order`.`name` AS `sales_order`,
			`tabSales Order`.`customer` AS `customer`,
	
			`tabSales Order`.`delivery_date` AS `delivery_date`,
			`tabSales Order`.`tracking_number` AS `tracking_number`,
			`tabSales Order`.`modified` AS `tarcking_updated`,
			`tabSales Order`.`courier_partner` AS `courier_partner`,
			`tabSales Order`.`type` AS `type`,
			`tabSales Order`.`total` AS `total`,
			`tabSales Order`.`total_shipment_weight` AS `total_shipment_weight`,
			`tabSales Order`.`total_qty` AS `total_qty`,
			`tabSales Order`.`shipping_status` AS `shipping_status`,
			`tabSales Order`.`shipping_address_name` AS `shipping_address_name`,
			`tabSales Order`.`shipping_address` AS `shipping_address`
			FROM `tabSales Order`
			WHERE {0} """.format(conditions),
		filters,
	)
	
	if len(data_sql) == 0:
		frappe.msgprint("No data found")
		return [], []
	
	if len(data_sql) == 0:
		frappe.msgprint("No data found")
		return [], []

	columns = [
		{
			"label": "Sales Order",
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 150
		},
		{
			"label": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},

		{
			"label": "Delivery Date",
			"fieldname": "delivery_date",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": "Tracking Number",
			"fieldname": "tracking_number",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Tracking Updated",
			"fieldname": "tarcking_updated",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": "Courier Partner",
			"fieldname": "courier_partner",
			"fieldtype": "Data",
			"width": 150

		},
  		{
        "label": "Type",
        "fieldname": "type",
        "fieldtype": "Data",
        "width": 150
        
      	},
		{
			"label": "Total",
			"fieldname": "total",
			"fieldtype": "Currency",
			"width": 150

		},
		{
			"label": "Total Shipment Weight",
			"fieldname": "total_shipment_weght",
			"fieldtype": "Float",
			"width": 150

		
		},
		{
			"label": "Total Qty",
			"fieldname": "total_qty",
			"fieldtype": "Int",
			"width": 150
		},
		{
		
			"label": "Shipping Status",
			"fieldname": "shipping_status",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Shipping Address Name",
			"fieldname": "shipping_address_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": "Shipping Address",
			"fieldname": "shipping_address",
			"fieldtype": "Data",
			"width": 150
		},
	]

	return columns, data_sql

# def get_condition(filters):
# 	conditions = ""
# 	if filters.get("sales_order"):
# 		conditions = "`tabSales Order`.`name` = '{0}'".format(filters.get("sales_order"))
# 	if filters.get("from_date") and filters.get("to_date"):
# 		conditions = "`tabSales Order`.`delivery_date` BETWEEN '{0}' AND '{1}'".format(filters.get("from_date"), filters.get("to_date"))
# 	if filters.get("customer"):
# 		conditions = "`tabSales Order`.`customer` = '{0}'".format(filters.get("customer"))
# 	if filters.get("type"):
# 		conditions = "`tabSales Order`.`type` = '{0}'".format(filters.get("type"))
# 	if filters.get("tracking_no"):
# 		conditions = "`tabSales Order`.`tracking_number` = '{0}'".format(filters.get("tracking_no"))
# 	return conditions

def get_condition(filters):
    condition = ""
    if filters.get("from_date") and filters.get("to_date"):
        if filters.get("shipping_status"):
            condition = "`tabSales Order`.`shipping_status` = '{0}' AND `tabSales Order`.`delivery_date` BETWEEN '{1}' AND '{2}'".format(filters.get("shipping_status"), filters.get("from_date"), filters.get("to_date"))
        elif filters.get("type"):
            condition = "`tabSales Order`.`type` = '{0}' AND `tabSales Order`.`delivery_date` BETWEEN '{1}' AND '{2}'".format(filters.get("type"), filters.get("from_date"), filters.get("to_date"))
           
        else:
            condition = "`tabSales Order`.`delivery_date` BETWEEN '{0}' AND '{1}'".format(filters.get("from_date"), filters.get("to_date"))

		
			
            
    return condition