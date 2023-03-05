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
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": [
				
				{"label": "Domestic", "value": "Domestic"},
				{"label": "International", "value": "International"},
		
			],
		}
	]
};