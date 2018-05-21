# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "palazon"
app_title = "Palazon"
app_publisher = "GreyCube Technologies"
app_description = "get BOM Item Rate based on summation of their individual line item"
app_icon = "octicon octicon-screen-full"
app_color = "#a00808"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/palazon/css/palazon.css"
# app_include_js = "/assets/palazon/js/palazon.js"

# include js, css files in header of web template
# web_include_css = "/assets/palazon/css/palazon.css"
#web_include_js = "/assets/palazon/js/palazon.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {"Sales Order" : "public/js/sales_order_client.js"}
doctype_js = {"Quotation" : "public/js/quotation_client.js"}
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "palazon.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "palazon.install.before_install"
# after_install = "palazon.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "palazon.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"palazon.tasks.all"
# 	],
# 	"daily": [
# 		"palazon.tasks.daily"
# 	],
# 	"hourly": [
# 		"palazon.tasks.hourly"
# 	],
# 	"weekly": [
# 		"palazon.tasks.weekly"
# 	]
# 	"monthly": [
# 		"palazon.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "palazon.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "palazon.event.get_events"
# }

fixtures = [
    # 	{
	# 	"dt":"Custom Script",
	# 	"filters":[
	# 		["name", "in", [
	# 		"Sales Order-Client"]],
	# 	]
	# },
	{
	"dt":"Print Format",
			"filters":[
			["name", "in", [
			"PrintBOM","Quot BOM"]],
		]
	}
]