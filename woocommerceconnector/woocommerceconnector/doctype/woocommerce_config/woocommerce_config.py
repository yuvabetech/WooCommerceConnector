# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


# The following is a list of the methods in the WooCommerceConfig class:

# The WooCommerceConfig class is a Frappe document that represents the configuration settings for a WooCommerce integration. It contains a validate method that is called when the document is saved, which in turn calls the check_stores_settings and validate_access methods.
# The check_stores_settings method checks that at least one WooCommerce store is configured, and that each store has a URL, API key, and API secret configured.
# The validate_access method attempts to make a test request to the WooCommerce API using the configured credentials, and raises an exception if the request fails.
# The get_series function is a Frappe whitelisted function that returns a dictionary of naming series for various document types.


from __future__ import unicode_literals
import frappe
from frappe import _
import requests.exceptions
from frappe.model.document import Document
from woocommerceconnector.woocommerce_requests import get_request
from woocommerceconnector.exceptions import woocommerceSetupError

class WooCommerceConfig(Document):
    def validate(self):
        if self.enable_woocommerce == 1:
            # self.validate_access_credentials()
            self.check_stores_settings()
            # self.validate_access()


    def check_stores_settings(self):
            
        if len(self.woocommerce_store_settings) == 0:
            frappe.msgprint(_("""Please make sure you have one atleat one  woocommerce store  config"""))
        else:
            for settings in self.woocommerce_store_settings:
                if not settings.woocommerce_url:
                    frappe.msgprint(_("""Please make sure you have one atleat one  woocommerce store  URL If you do not have one, please create one in your woocommerce account. If you have one, please make sure it is correct."""))
                    break
                if not settings.api_key:
                    frappe.msgprint(_("""Please make sure you have  API key  If you do not have one, please create one in your woocommerce account. If you have one, please make sure it is correct."""))
                    break
                if not settings.api_secret:
                    frappe.msgprint(_("""Please make sure you have one atleat one  woocommerce store  API secret. If you do not have one, please create one in your woocommerce account. If you have one, please make sure it is correct."""))
                    break



    def validate_access(self):
        try:
            r = get_request('settings', {"api_key": self.api_key,
                "api_secret": self.get_password(fieldname='api_secret',raise_exception=False), "woocommerce_url": self.woocommerce_url, "verify_ssl": self.verify_ssl})

        except requests.exceptions.HTTPError:
            # disable woocommerce!
            frappe.db.rollback()
            self.set("enable_woocommerce", 0)
            frappe.db.commit()

            frappe.throw(_("""Error Validating API"""), woocommerceSetupError)


@frappe.whitelist()
def get_series():
        return {
            "sales_order_series" : frappe.get_meta("Sales Order").get_options("naming_series") or "SO-woocommerce-",
            "sales_invoice_series" : frappe.get_meta("Sales Invoice").get_options("naming_series")  or "SI-woocommerce-",
            "delivery_note_series" : frappe.get_meta("Delivery Note").get_options("naming_series")  or "DN-woocommerce-",
            "item_code_naming_series" : frappe.get_meta("Item").get_options("naming_series")  or "Item-woocommerce-"
        }
