# Copyright (c) 2023, libracore and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	so = frappe.db.sql("""SELECT
			`tabSales Order`.`name` AS `sales_order`,
			`tabSales Order`.`customer` AS `customer`,
			`tabSales Order`.`customer_name` AS `customer_name` ,
			`tabSales Order`.`delivery_date` AS `delivery_date`,
			`tabSales Order`.`tracking_number` AS `tracking_number`,
			`tabSales Order`.`courier_partner` AS `courier_partner`,
			`tabSales Order`.`total` as `total`,
			`tabSales Order`.`total_qty` AS `total_qty`,
			`tabSales Order`.`shipping_status` AS `shipping_status`,
			`tabSales Order`.`shipping_address_name` AS `shipping_address_name`,
			`tabSales Order`.`shipping_address` AS `shipping_address`,
			`tabSales Order`. `modified` as `tracking_updated`

			FROM `tabSales Order`
			WHERE `tabSales Order`.`type` = %(type)s
			OR `tabSales Order`.`customer` = %(customer)s
			OR  `tabSales Order`. `creation` >= %(from_date)s
			

		

		
			""",{
						"customer": filters.get("customer"),
				"type": filters.get("type"),
				"from_date": filters.get("from_date"),
			}, as_dict=1)

	data = so
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
			"label": "Customer Name",
			"fieldname": "customer_name",
			"fieldtype": "Data",
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
			"label": "Total",
			"fieldname": "total",
			"fieldtype": "Currency",
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

	return columns, data
