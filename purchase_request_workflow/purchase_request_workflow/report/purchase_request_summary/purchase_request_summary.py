# Copyright (c) 2026, arise and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, getdate, nowdate

def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)
	report_summary = get_report_summary(data)
	return columns, data, None, chart, report_summary

def get_columns():
	"""Columns displayed in the report grid."""
	return [
		{"label": "ID", "fieldname": "name", "fieldtype": "Link", "options": "Purchase Request", "width": 140},
		{"label": "Title", "fieldname": "title", "fieldtype": "Data", "width": 180},
		{"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data", "width": 130},
		{"label": "Requester", "fieldname": "requester", "fieldtype": "Link", "options": "User", "width": 160},
		{"label": "Department", "fieldname": "department", "fieldtype": "Data", "width": 130},
		{"label": "Required By", "fieldname": "required_by", "fieldtype": "Date", "width": 120},
		{"label": "Estimated Total", "fieldname": "estimated_total", "fieldtype": "Currency", "width": 140},
		{"label": "Supplier", "fieldname": "supplier", "fieldtype": "Data", "width": 140},
		{"label": "Order Date", "fieldname": "order_date", "fieldtype": "Date", "width": 120}
	]

def get_data(filters):
	"""Fetch data from MariaDB applying selected filters."""
	conditions = []
	values = {}

	if filters.get("workflow_state"):
		conditions.append("workflow_state = %(workflow_state)s")
		values["workflow_state"] = filters["workflow_state"]

	if filters.get("department"):
		conditions.append("department LIKE %(department)s")
		values["department"] = f"%{filters['department']}%"

	if filters.get("requester"):
		conditions.append("requester = %(requester)s")
		values["requester"] = filters["requester"]

	if filters.get("from_date"):
		conditions.append("creation >= %(from_date)s")
		values["from_date"] = filters["from_date"]

	if filters.get("to_date"):
		conditions.append("creation <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	query = f"""
		SELECT 
			name, title, workflow_state, requester, department, 
			required_by, estimated_total, supplier, order_date, creation
		FROM `tabPurchase Request`
		{where_clause}
		ORDER BY creation DESC
	"""
	return frappe.db.sql(query, values, as_dict=True)

def get_chart(data):
	"""Render a visual bar chart of Estimated Spend by Department."""
	if not data:
		return None

	dept_totals = {}
	for row in data:
		dept = row.get("department") or "Unassigned"
		dept_totals[dept] = dept_totals.get(dept, 0.0) + flt(row.get("estimated_total"))

	return {
		"data": {
			"labels": list(dept_totals.keys()),
			"datasets": [{"name": "Estimated Spend", "values": list(dept_totals.values())}]
		},
		"type": "bar",
		"colors": ["#5e64ff", "#29b380", "#ffa00a", "#ff5858"]
	}

def get_report_summary(data):
	"""Render 4 executive KPI summary cards above the report."""
	if not data:
		return []

	total_requests = len(data)
	total_spend = sum(flt(d.get("estimated_total")) for d in data)
	pending_approvals = sum(1 for d in data if d.get("workflow_state") == "Submitted")

	today = getdate(nowdate())
	overdue = sum(
		1 for d in data 
		if d.get("required_by") and getdate(d.get("required_by")) < today and d.get("workflow_state") != "Received"
	)

	return [
		{"value": total_requests, "label": "Total Requests", "datatype": "Int", "indicator": "Blue"},
		{"value": total_spend, "label": "Total Estimated Spend", "datatype": "Currency", "indicator": "Green"},
		{"value": pending_approvals, "label": "Pending Approvals", "datatype": "Int", "indicator": "Orange"},
		{"value": overdue, "label": "Overdue Requests", "datatype": "Int", "indicator": "Red"}
	]