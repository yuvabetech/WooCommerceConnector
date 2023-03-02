# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# t implements functions related to syncing data between ERPNext and WooCommerce.
# The sync_woocommerce function is used to enqueue a long job for syncing WooCommerce data. The function sync_woocommerce_resources is the actual function that performs the sync process. This function first fetches the store settings for the specified store name and then validates the WooCommerce settings. It then proceeds to sync products, customers, and orders, and updates the stock quantity of items if the option is enabled. If the sync process fails, it logs the error and disables the sync until the issue is resolved.
# The check_hourly_sync function checks if the hourly sync is enabled in the WooCommerce settings, and if so, it calls the sync_woocommerce function.
# The get_log_status function returns the status of the last sync job performed, whether it was successful, failed, or queued.

from __future__ import unicode_literals
import frappe
from frappe import _
from .exceptions import woocommerceError
from .sync_orders import sync_orders, close_synced_woocommerce_orders,close_synced_woocommerce_order
from .sync_customers import sync_customers
from .sync_products import sync_products, update_item_stock_qty
from .utils import disable_woocommerce_sync_on_exception, make_woocommerce_log
from frappe.utils.background_jobs import enqueue
from .woocommerce_requests import  put_request
import requests
@frappe.whitelist()
def update_wc_order(status,wc_order_id,store_name):
    # return status,wc_order_id,store_name
    order_data = {
        "status": status
    }
    try:
       return put_request("orders/{0}".format(wc_order_id), order_data,store_name)
            
    except requests.exceptions.HTTPError as e:
        make_woocommerce_log(title=e.message, status="Error", method="close_synced_woocommerce_order", message=frappe.get_traceback(),
            request_data=woocommerce_order, exception=True)



@frappe.whitelist()
def get_store_settings(store_name):
    db = frappe.db.sql("""select name, woocommerce_url, api_key, api_secret, verify_ssl, price_list from `tabWoocommerce Store Settings` where woocommerce_url = %s""", store_name,as_dict=1)
    return db

#############################################
@frappe.whitelist()
def check_hourly_sync():
    woocommerce_settings = frappe.get_doc("WooCommerce Config")
    if woocommerce_settings.hourly_sync == 1:
        sync_woocommerce()

@frappe.whitelist()
def sync_woocommerce(store=None):
    # sync_woocommerce_resources(store)
    """Enqueue longjob for syncing woocommerce"""
    woocommerce_settings = frappe.get_doc("WooCommerce Config")
    if woocommerce_settings.sync_timeout == 0:
        woocommerce_settings.sync_timeout = 1500
        woocommerce_settings.save()
    timeout = woocommerce_settings.sync_timeout or 1500
    # apply minimal timeout of 60 sec
    if timeout < 60:
        timeout = 60
    enqueue("woocommerceconnector.api.sync_woocommerce_resources",store=store, queue='long', timeout=timeout)
    frappe.msgprint(_("Queued for syncing. It may take a few minutes to an hour if this is your first sync."))

@frappe.whitelist()
def sync_woocommerce_resources(store):

    woocommerce_settings = frappe.get_doc("WooCommerce Config")
    store_settings = get_store_settings(store)
    price_list = store_settings[0].get('price_list')
    store_name = store_settings[0].get('woocommerce_url')
    print("store_name",store_name,price_list)


    make_woocommerce_log(title="Sync Job Queued", status="Queued", method=frappe.local.form_dict.cmd, message="Sync Job Queued")
    
    if woocommerce_settings.enable_woocommerce:
        make_woocommerce_log(title="Sync Job Started  ", status="Started", method=frappe.local.form_dict.cmd, message="Sync Job Started")
        try :
            validate_woocommerce_settings(woocommerce_settings)
            sync_start_time = frappe.utils.now()
            frappe.local.form_dict.count_dict = {}
            frappe.local.form_dict.count_dict["customers"] = 0
            frappe.local.form_dict.count_dict["products"] = 0
            frappe.local.form_dict.count_dict["orders"] = 0
            sync_products(store_name,price_list, woocommerce_settings.warehouse, True if woocommerce_settings.sync_items_from_woocommerce_to_erp == 1 else False)
            sync_customers(store_name)
            sync_orders(store_name)
            # close_synced_woocommerce_orders() # DO NOT GLOBALLY CLOSE
            if woocommerce_settings.sync_item_qty_from_erpnext_to_woocommerce:
                update_item_stock_qty()
            frappe.db.set_value("WooCommerce Config", None, "last_sync_datetime", sync_start_time)
            make_woocommerce_log(title="Sync Completed", status="Success", method=frappe.local.form_dict.cmd, 
                message= "Updated {customers} customer(s), {products} item(s), {orders} order(s)".format(**frappe.local.form_dict.count_dict))

        except Exception as e:
            if e.args[0] and hasattr(e.args[0], "startswith") and e.args[0].startswith("402"):
                make_woocommerce_log(title="woocommerce has suspended your account", status="Error",
                    method="sync_woocommerce_resources", message=_("""woocommerce has suspended your account till
                    you complete the payment. We have disabled ERPNext woocommerce Sync. Please enable it once
                    your complete the payment at woocommerce."""), exception=True)

                disable_woocommerce_sync_on_exception()
            
            else:
                make_woocommerce_log(title="sync has terminated", status="Error", method="sync_woocommerce_resources",
                    message=frappe.get_traceback(), exception=True)
                    
    elif frappe.local.form_dict.cmd == "woocommerceconnector.api.sync_woocommerce":
        make_woocommerce_log(
            title="woocommerce connector is disabled",
            status="Error",
            method="sync_woocommerce_resources",
            message=_("""woocommerce connector is not enabled. Click on 'Connect to woocommerce' to connect ERPNext and your woocommerce store."""),
            exception=True)

def validate_woocommerce_settings(woocommerce_settings):
    """
        This will validate mandatory fields and access token or app credentials 
        by calling validate() of WooCommerce Config.
    """
    try:
        woocommerce_settings.save()
    except woocommerceError:
        disable_woocommerce_sync_on_exception()

@frappe.whitelist()
def get_log_status():
    log = frappe.db.sql("""select name, status from `tabwoocommerce Log` 
        order by modified desc limit 1""", as_dict=1)
    if log:
        if log[0].status=="Queued":
            message = _("Last sync request is queued")
            alert_class = "alert-warning"
        elif log[0].status=="Error":
            message = _("Last sync request was failed, check <a href='../desk#Form/woocommerce Log/{0}'> here</a>"
                .format(log[0].name))
            alert_class = "alert-danger"
        else:
            message = _("Last sync request was successful")
            alert_class = "alert-success"
            
        return {
            "text": message,
            "alert_class": alert_class
        }
        
@frappe.whitelist()
def sync_woocommerce_ids():
    "Enqueue longjob for syncing woocommerce"
    enqueue("woocommerceconnector.sync_products.add_w_id_to_erp", queue='long', timeout=1500)
    frappe.msgprint(_("Queued for syncing. It may take a few minutes to an hour if this is your first sync."))
