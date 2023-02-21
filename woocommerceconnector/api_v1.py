# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from .exceptions import woocommerceError
from .sync_orders import sync_orders, close_synced_woocommerce_orders
from .sync_customers import sync_customers
from .sync_products import sync_products, update_item_stock_qty
from .utils import disable_woocommerce_sync_on_exception, make_woocommerce_log
from frappe.utils.background_jobs import enqueue

################ New Implimentations

@frappe.whitelist()       
def get_store_settings(store_name):
    st = frappe.get_all("Woocommerce Store Settings",
    filters={"woocommerce_url": store_name},fields=["name", "woocommerce_url", "api_key", "api_secret", "verify_ssl"])
    return st
#############################################
@frappe.whitelist()
def check_hourly_sync():
    woocommerce_settings = frappe.get_doc("WooCommerce Config")
    if woocommerce_settings.hourly_sync == 1:
        sync_woocommerce()

@frappe.whitelist()
def sync_woocommerce(store):
    """Enqueue longjob for syncing woocommerce"""
    woocommerce_settings = frappe.get_doc("WooCommerce Config")
    if woocommerce_settings.sync_timeout == 0:
        woocommerce_settings.sync_timeout = 1500
        woocommerce_settings.save()
    timeout = woocommerce_settings.sync_timeout or 1500
    # apply minimal timeout of 60 sec
    if timeout < 60:
        timeout = 60
    enqueue("woocommerceconnector.api_v1.sync_woocommerce_resources",store=store, queue='short', timeout=timeout)
    frappe.msgprint(_("Queued for syncing. It may take a few minutes to an hour if this is your first sync."))

@frappe.whitelist()
def sync_woocommerce_resources(store=None):
    print("store",store)
