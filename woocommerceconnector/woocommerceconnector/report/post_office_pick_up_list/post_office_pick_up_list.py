# Copyright (c) 2023, libracore and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = [], []
    conditions = get_condition(filters)
    print("Conditions: {0}".format(conditions))
    data_sql = frappe.db.sql(
    """SELECT
       `tabSales Invoice`.`address_display` AS `address_display`,
        `tabSales Invoice`.`posting_date` AS `posting_date`,
       `tabSales Invoice`.`tracking_number` AS `tracking_number`,
       `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`

        FROM `tabSales Invoice`
        WHERE {0} AND `tabSales Invoice`.`tracking_number` IS NOT NULL AND `tabSales Invoice`.`tracking_number` != ''
        """.format(conditions),
    filters,
)

    # data_sql = frappe.db.sql(
    #     """SELECT
    #        `tabSales Invoice`.`address_display` AS `address_display`,
    #         `tabSales Invoice`.`posting_date` AS `posting_date`,
    #        `tabSales Invoice`.`tracking_number` AS `tracking_number`

    #         FROM `tabSales Invoice`
    #         WHERE {0} """.format(conditions),
    #     filters,
    # )
	

    if not data_sql:
        frappe.msgprint("No data found")
        return [], []

    columns = [
              {
            "label": "Address",
            "fieldname": "address_display",
            "fieldtype": "Data",
        
            "width": 150
        },{
               "label": "Sent Date",
            "fieldname": "posting_date",
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
                    "label": "Weight",
            "fieldname": "total_shipment_weight",
            "fieldtype": "Data",
        
            "width": 150
        
		}
 

    ]

    return columns, data_sql

def get_condition(filters):
    condition = ""
    if filters.get("from_date") and filters.get("to_date"):
        if filters.get("sales_channel"):
            condition = "`tabSales Invoice`.`sales_channel` = '{0}' AND `tabSales Invoice`.`posting_date` BETWEEN '{1}' AND '{2}'".format(filters.get("sales_channel"), filters.get("from_date"), filters.get("to_date"))
        elif filters.get("type"):
            condition = "`tabSales Invoice`.`type` = '{0}' AND `tabSales Invoice`.`posting_date` BETWEEN '{1}' AND '{2}'".format(filters.get("type"), filters.get("from_date"), filters.get("to_date"))
        else:
            condition = "`tabSales Invoice`.`posting_date` BETWEEN '{0}' AND '{1}'".format(filters.get("from_date"), filters.get("to_date"))

    return condition
