// Copyright (c) 2023, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pick up post office list"] = {
	"filters": [
	

		{
			"fieldname":"from_date",
			"label": __(" From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1)
		},
		{
			"fieldname":"to_date",
			"label": __("To  Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1)
		}
		,
		{
			"fieldname":"shipping_status",
			"label": __("Shipping Status"),
			"fieldtype": "Select",
			"options": [
			
				{"label": "Yet to Confirm", "value": "Yet to Confirm"},
				{"label": "Awaiting Payment", "value": "Awaiting Payment"},
				{"label": "Payment Received", "value": "Payment Received"},
				{"label": "Shipped", "value": "Shipped"},
				{"label": "Delivered", "value": "Delivered"}

			]
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": [
				
				{"label": "Domestic", "value": "Domestic"},
				{"label": "International", "value": "International"},
				{"label": "Domestic Dropshipping" , "value": "Domestic Dropshipping"},
				{"label": "Domestic Stock" , "value": "Domestic Stock"},
				{"label": "Office Sale" , "value": "Office Sale"},
				{"label": "Open House" , "value": "Open House"},
				{"label": "Workshop" , "value": "Workshop"},
				{"label": "Event" , "value": "Event"},
				{"label": "Pad for Pad" , "value": "Pad for Pad"},
				{"label": "Pad for Sisters" , "value": "Pad for Sisters"},
				{"label": "Direct" , "value": "Direct"},
				{"label": "Partner" , "value": "Partner"},
				{"label": "Rural Subsidised" , "value": "Rural Subsidised"},
				{"label": "Rural Cost price" , "value": "Rural Cost price"},
				{"label": "Rural Direct" , "value": "Rural Direct"},
				{"label": "Rural Retailers" , "value": "Rural Retailers"}
			],
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		}
	]
};