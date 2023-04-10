// Copyright (c) 2023, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Post Office Pick Up List"] = {
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
		},
		{
			"fieldname":"options",
			"label": __("Options"),
			"fieldtype": "Select",
			"options": "With Tracking\nWithout Tracking",
			"default": "All"
		},
		
	]
};
