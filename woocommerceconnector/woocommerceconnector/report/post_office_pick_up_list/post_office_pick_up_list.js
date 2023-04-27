// Copyright (c) 2023, libracore and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Post Office Pick Up List"] = {
	"filters": [
	

		{
			"fieldname":"from_date",
			"label": __(" From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"to_date",
			"label": __("To  Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"options",
			"label": __("Options"),
			"fieldtype": "Select",
	
			"options": [
				
				{"label": "Tracking", "value": "Tracking"},
				{"label": "Without Tracking", "value": "Without Tracking"}
				
			]
		},
		
	]
};
