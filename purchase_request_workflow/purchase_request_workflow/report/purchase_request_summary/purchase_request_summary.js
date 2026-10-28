// Copyright (c) 2026, arise and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Request Summary"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "workflow_state",
			"label": __("Status"),
			"fieldtype": "Link",
			"options": "Workflow State"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "requester",
			"label": __("Requester"),
			"fieldtype": "Link",
			"options": "User"
		}
	]
};