// Copyright (c) 2023, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pick up post office list"] = {
	"filters": [
		{
			"fieldname":"sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
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
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": [
				
				{"label": "Domestic", "value": "Domestic"},
				{"label": "International", "value": "International"},
		
			],
		},
		{
			"fieldname":"tracking_no",
			"label": __("Tracking No."),
			"fieldtype": "Data"
		}
	]
};