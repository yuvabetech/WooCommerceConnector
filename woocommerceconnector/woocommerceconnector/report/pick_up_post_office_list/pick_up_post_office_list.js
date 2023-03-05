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