// Copyright (c) 2023, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pick up post office list"] = {
	"filters": [
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"from_date",
			"label": __(" Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": [
				{"label": "All", "value": "All"},
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