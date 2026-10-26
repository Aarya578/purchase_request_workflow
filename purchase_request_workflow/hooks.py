from . import __version__ as app_version

app_name = "purchase_request_workflow"
app_title = "Purchase Request Workflow"
app_publisher = "Aarya"
app_description = "Purchase Request workflow System"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "ak2003@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/purchase_request_workflow/css/purchase_request_workflow.css"
# app_include_js = "/assets/purchase_request_workflow/js/purchase_request_workflow.js"

# include js, css files in header of web template
# web_include_css = "/assets/purchase_request_workflow/css/purchase_request_workflow.css"
# web_include_js = "/assets/purchase_request_workflow/js/purchase_request_workflow.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "purchase_request_workflow/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "purchase_request_workflow.install.before_install"
# after_install = "purchase_request_workflow.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "purchase_request_workflow.uninstall.before_uninstall"
# after_uninstall = "purchase_request_workflow.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "purchase_request_workflow.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"purchase_request_workflow.tasks.all"
#	],
#	"daily": [
#		"purchase_request_workflow.tasks.daily"
#	],
#	"hourly": [
#		"purchase_request_workflow.tasks.hourly"
#	],
#	"weekly": [
#		"purchase_request_workflow.tasks.weekly"
#	]
#	"monthly": [
#		"purchase_request_workflow.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "purchase_request_workflow.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "purchase_request_workflow.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "purchase_request_workflow.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["purchase_request_workflow.utils.before_request"]
# after_request = ["purchase_request_workflow.utils.after_request"]

# Job Events
# ----------
# before_job = ["purchase_request_workflow.utils.before_job"]
# after_job = ["purchase_request_workflow.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"purchase_request_workflow.auth.validate"
# ]

