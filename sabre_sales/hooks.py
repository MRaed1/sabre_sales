app_name = "sabre_sales"
app_title = "Sabre Sales"
app_publisher = "Main Telecom"
app_description = "Sabre Sales Workflow Management"
app_email = "m.raed@cx3.me"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sabre_sales",
# 		"logo": "/assets/sabre_sales/logo.png",
# 		"title": "Sabre Sales",
# 		"route": "/sabre_sales",
# 		"has_permission": "sabre_sales.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sabre_sales/css/sabre_sales.css"
# app_include_js = "/assets/sabre_sales/js/sabre_sales.js"

# include js, css files in header of web template
# web_include_css = "/assets/sabre_sales/css/sabre_sales.css"
# web_include_js = "/assets/sabre_sales/js/sabre_sales.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sabre_sales/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sabre_sales/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
    "Sabre Account Manager": "sabre-sales",
    "Sabre Finance Manager": "sabre-sales",
    "Sabre Head Of Sales":"sabre-sales"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sabre_sales.utils.jinja_methods",
# 	"filters": "sabre_sales.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sabre_sales.install.before_install"
# after_install = "sabre_sales.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sabre_sales.uninstall.before_uninstall"
# after_uninstall = "sabre_sales.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sabre_sales.utils.before_app_install"
# after_app_install = "sabre_sales.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sabre_sales.utils.before_app_uninstall"
# after_app_uninstall = "sabre_sales.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sabre_sales.notifications.get_notification_config"

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
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sabre_sales.tasks.all"
# 	],
# 	"daily": [
# 		"sabre_sales.tasks.daily"
# 	],
# 	"hourly": [
# 		"sabre_sales.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sabre_sales.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sabre_sales.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sabre_sales.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "sabre_sales.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sabre_sales.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sabre_sales.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sabre_sales.utils.before_request"]
# after_request = ["sabre_sales.utils.after_request"]

# Job Events
# ----------
# before_job = ["sabre_sales.utils.before_job"]
# after_job = ["sabre_sales.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sabre_sales.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

fixtures = [
    {
        "doctype": "DocType",
        "filters": [["module", "=", "Sabre Sales"]]
    },
    {
        "doctype": "Server Script",
        "filters": [["module", "=", "Sabre Sales"]]
    },
    {
        "doctype": "Client Script",
        "filters": [["module", "=", "Sabre Sales"]]
    },
    {
        "doctype": "Workflow",
        "filters": [["document_type", "=", "Sabre Sales Opportunity"]]
    },
    {
        "doctype": "Notification",
        "filters": [["module", "=", "Sabre Sales"]]
    }
]

fixtures += [
    {
        "doctype": "Dashboard",
        "filters": [["module", "=", "Sabre Sales"]]
    },
    {
        "doctype": "Number Card",
        "filters": [["module", "=", "Sabre Sales"]]
    },
    {
        "doctype": "Dashboard Chart",
        "filters": [["module", "=", "Sabre Sales"]]
    }
]

fixtures += [
    {
        "doctype": "Workspace",
        "filters": [["module", "=", "Sabre Sales"]]
    }
]

fixtures += [
    {
        "doctype": "Print Format",
        "filters": [["module", "=", "Sabre Sales"]]
    }
]
fixtures += [
    {
        "doctype": "Role",
        "filters": [["name", "in", ["Sabre Account Manager", "Sabre Finance Manager", "Sabre Head Of Sales"]]]
    },
    {
        "doctype": "Custom DocPerm",
        "filters": [["parent", "in", [
            "Sabre Sales Opportunity",
            "Sabre Qualification Checklist",
            "Sabre Business Case",
            "Sabre Contract",
            "Sabre Implementation",
            "Sabre Go-Live"
        ]]]
    }
]
after_migrate = ["sabre_sales.setup.import_workspace"]
