import frappe
from datetime import datetime

def execute(filters=None):
    columns = [
        {
            "label": "Address Name",
            "fieldname": "customer_address",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Address",
            "fieldname": "address_display",
            "fieldtype": "Data",
            "width": 150
        },
        {
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
    data = []
    conditions = ""
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " `tabSales Invoice`.`posting_date` BETWEEN '{0}' AND '{1}' ".format(filters.get("from_date"), filters.get("to_date"))
    
    if filters.get("options") == "With Tracking":
        conditions += " AND `tabSales Invoice`.`tracking_number` IS NOT NULL AND `tabSales Invoice`.`tracking_number` != '' "
    elif filters.get("options") == "Without Tracking":
        conditions += " AND (`tabSales Invoice`.`tracking_number` IS NULL OR `tabSales Invoice`.`tracking_number` = '') "

    today = datetime.today().strftime('%Y-%m-%d')
    conditions += " AND `tabSales Invoice`.`docstatus` = 1 AND `tabSales Invoice`.`posting_date` = '{0}' ".format(today)

    query = """
        SELECT
            `tabSales Invoice`.`customer_address` AS `customer_address`,
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`
        FROM `tabSales Invoice`
        WHERE {0}
        AND `tabSales Invoice`.`sales_channel` = 'B2C' AND `tabSales Invoice`.`type` = 'Domestic'
        LIMIT 100 OFFSET 0

        UNION ALL

        SELECT
            `tabSales Invoice`.`customer_address` AS `customer_address`,
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`
        FROM `tabSales Invoice`
        WHERE {0}
        AND `tabSales Invoice`.`sales_channel` = 'B2C' AND `tabSales Invoice`.`type` = 'International'
        LIMIT 100 OFFSET 0

        UNION ALL

        SELECT
            `tabSales Invoice`.`customer_address` AS `customer_address`,
            `tabSales Invoice`.`address_display` AS `address_display`,
            `tabSales Invoice`.`posting_date` AS `posting_date`,
            `tabSales Invoice`.`tracking_number` AS `tracking_number`,
            `tabSales Invoice`.`total_shipment_weight` AS `total_shipment_weight`
        FROM `tabSales Invoice`
        WHERE {0} AND `tabSales Invoice`.`sales_channel` = 'Retailers' AND `tabSales Invoice`.`type` = 'International'
        LIMIT 100 OFFSET 0
    """.format(conditions)

    data_sql = frappe.db.sql(query, as_dict=True)

    if not data_sql:
        frappe.msgprint("No data found")
        return [], []

    return columns, data_sql