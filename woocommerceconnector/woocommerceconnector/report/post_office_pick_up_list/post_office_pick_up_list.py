# Copyright (c) 2023, libracore and contributors
# For license information, please see license.txt

import frappe

def get_sales_invoice_tracking_data(date):
    conditions = "`tabSales Invoice`.docstatus = 1 AND `tabSales Invoice`.posting_date = '{0}'".format(date)
    query = ''

    data_sql = frappe.db.sql(query, as_list=True)

    # insert empty rows between partitions
    empty_row = ['']*5
    for i in range(1, len(data_sql), 6):
        data_sql.insert(i, empty_row)

    return data_sql
def execute(filters=None):
    columns, data = [], []
    conditions = get_condition(filters)
    print("Conditions: {0}".format(conditions))
    data_sql = frappe.db.sql(
		"""SELECT  'Domestic air post (Domestic Parcels)',NULL, NULL, NULL, NULL

    UNION ALL
    SELECT *
    FROM
    (
        SELECT
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`,
            Null AS `rs`
        FROM `tabSales Invoice`
        WHERE ({0}) AND (`sales_channel` = 'B2C' AND `type` = 'Domestic')
        AND `tabSales Invoice`.`tracking_number` IS NOT NULL AND `tabSales Invoice`.`tracking_number` != ''
        ORDER BY `posting_date` ASC
        LIMIT 100 OFFSET 0
    ) AS a

    UNION ALL

    SELECT  'Registered air parcel (INTERNATIONAL small parcels)',NULL, NULL, NULL, NULL

    UNION ALL

    SELECT *
    FROM
    (
        SELECT
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`,
            Null AS `rs`
        FROM `tabSales Invoice`
        WHERE ({0}) AND (`sales_channel` = 'B2C' AND `type` = 'International')
        AND `tabSales Invoice`.`tracking_number` IS NOT NULL AND `tabSales Invoice`.`tracking_number` != ''
        ORDER BY `posting_date` ASC
        LIMIT 100 OFFSET 0
    ) AS b

    UNION ALL

    SELECT 'Registered air parcel (INTERNATIONAL big boxes)',NULL, NULL, NULL, NULL

    UNION ALL

    SELECT *
    FROM
    (
        SELECT
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`,
            Null AS `rs`
        FROM `tabSales Invoice`
        WHERE ({0}) AND (`sales_channel` = 'Retailers' AND `type` = 'Domestic')
        AND `tabSales Invoice`.`tracking_number` IS NOT NULL AND `tabSales Invoice`.`tracking_number` != ''
        ORDER BY `posting_date` ASC
        LIMIT 100 OFFSET 0
    ) AS c""".format(conditions),
    filters
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
        condition = "`tabSales Invoice`.`posting_date` BETWEEN '{0}' AND '{1}'".format(filters.get("from_date"), filters.get("to_date"))

    return condition
