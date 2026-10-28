# -*- coding: utf-8 -*-
# Copyright (c) 2026, arise and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate, now_datetime

class PurchaseRequest(Document):
	def validate(self):
		self.validate_required_by_date()
		self.validate_items()
		self.calculate_totals()
		self.validate_approval_rules()
		self.process_receipts()
		
		# Auto-set order details if status is Ordered or beyond
		if self.workflow_state in ["Ordered", "Partially Received", "Received"]:
			if not self.order_date:
				self.order_date = nowdate()
			if not self.ordered_by:
				self.ordered_by = frappe.session.user

	def on_update(self):
		self.handle_workflow_notifications()

	def validate_required_by_date(self):
		"""Rule: Required-by date cannot be in the past."""
		if self.required_by and getdate(self.required_by) < getdate(nowdate()):
			frappe.throw("Required-by date cannot be in the past.")

	def validate_items(self):
		"""Rule: Require at least 1 item, positive qty, non-negative price."""
		if not self.items:
			frappe.throw("A Purchase Request must have at least one line item.")
		
		for row in self.items:
			if (row.qty or 0) <= 0:
				frappe.throw(f"Row {row.idx}: Quantity must be greater than zero.")
			if (row.estimated_rate or 0) < 0:
				frappe.throw(f"Row {row.idx}: Estimated Unit Price cannot be negative.")

	def calculate_totals(self):
		"""Recalculate line amounts and grand total on the server for safety."""
		total = 0.0
		for row in self.items:
			row.estimated_amount = (row.qty or 0.0) * (row.estimated_rate or 0.0)
			total += row.estimated_amount
		self.estimated_total = total

	def validate_approval_rules(self):
		"""Enforce segregation of duties and rejection comments."""
		state = self.get("workflow_state")
		
		# 1. Segregation of Duties: Requester cannot Approve OR Reject their own request!
		if state in ["Approved", "Rejected"]:
			if self.requester == frappe.session.user:
				frappe.throw(f"Segregation of Duties: You cannot {state.lower()} your own Purchase Request!")

			self.approver = frappe.session.user
			self.approval_date = now_datetime()

		# 2. Rejection must have a reason
		if state == "Rejected":
			if not (self.decision_comment and self.decision_comment.strip()):
				frappe.throw("A Decision Comment explaining the reason is mandatory when rejecting a request.")

	def process_receipts(self):
		"""Track goods receipts, update received qty, enforce over-receipt guard."""
		if not self.get("receipt_logs"):
			return

		# Sum received quantities by item_description
		received_totals = {}
		for log in self.receipt_logs:
			if (log.received_qty or 0) <= 0:
				frappe.throw(f"Receipt Log Row {log.idx}: Received Quantity must be greater than zero.")
			
			desc = (log.get("item_description") or log.get("item_reference") or "").strip()
			received_totals[desc] = received_totals.get(desc, 0.0) + float(log.received_qty)

		# Update each item row and check for over-receipt
		all_fully_received = True
		any_received = False

		for item in self.items:
			desc = (item.item_description or "").strip()
			tot_received = received_totals.get(desc, 0.0)
			
			# Over-receipt guard
			if tot_received > item.qty:
				frappe.throw(
					f"Over-Receipt Error for '{desc}': Total received ({tot_received}) "
					f"cannot exceed requested quantity ({item.qty})!"
				)
			
			item.received_qty = tot_received

			if tot_received < item.qty:
				all_fully_received = False
			if tot_received > 0:
				any_received = True

		# Auto-transition state based on receipts
		if self.workflow_state in ["Ordered", "Partially Received"]:
			if all_fully_received:
				self.workflow_state = "Received"
			elif any_received:
				self.workflow_state = "Partially Received"

	def handle_workflow_notifications(self):
		"""Show instant 3-second toast alert AND send persistent bell notification."""
		prev = self.get_doc_before_save()
		prev_state = prev.workflow_state if prev else None
		curr_state = self.workflow_state

		if prev_state == curr_state:
			return

		# 1. Submitted: Toast + Bell alert to Approvers & Admin
		if curr_state == "Submitted":
			msg = f"Purchase Request {self.name} submitted for Manager approval!"
			frappe.msgprint(msg, alert=True, indicator="blue")
			self.notify_roles(["Purchase Approver"], msg)
			self.notify_user("Administrator", msg)

		# 2. Approved: Toast + Bell alert to Requester & Admin
		elif curr_state == "Approved":
			msg = f"Purchase Request {self.name} approved! Ready for ordering."
			frappe.msgprint(msg, alert=True, indicator="green")
			self.notify_user(self.owner, msg)
			self.notify_user(self.requester, msg)
			self.notify_user("Administrator", msg)

		# 3. Rejected: Toast + Bell alert to Requester & Admin
		elif curr_state == "Rejected":
			msg = f"Purchase Request {self.name} rejected. Reason: {self.decision_comment}"
			frappe.msgprint(msg, alert=True, indicator="orange")
			self.notify_user(self.owner, msg)
			self.notify_user(self.requester, msg)
			self.notify_user("Administrator", msg)

		# 4. Ordered: Toast + Bell alert to Requester, Approver & Admin
		elif curr_state == "Ordered":
			msg = f"Purchase Order placed for {self.name}."
			frappe.msgprint(msg, alert=True, indicator="green")
			self.notify_user(self.owner, msg)
			self.notify_user(self.requester, msg)
			self.notify_user("Administrator", msg)

		# 5. Partially Received: Toast + Bell alert
		elif curr_state == "Partially Received":
			msg = f"Partial goods received for Purchase Request {self.name}."
			frappe.msgprint(msg, alert=True, indicator="blue")
			self.notify_user(self.owner, msg)
			self.notify_user("Administrator", msg)

		# 6. Received: Toast + Bell alert to Requester, Approver & Admin
		elif curr_state == "Received":
			msg = f"All goods received for Purchase Request {self.name}!"
			frappe.msgprint(msg, alert=True, indicator="green")
			self.notify_user(self.owner, msg)
			self.notify_user(self.requester, msg)
			if self.approver:
				self.notify_user(self.approver, msg)
			self.notify_user("Administrator", msg)

	def notify_user(self, user, subject):
		"""Send persistent alert to User's Bell Inbox."""
		if not user:
			return
		try:
			notif = frappe.new_doc("Notification Log")
			notif.for_user = user
			notif.from_user = frappe.session.user or "Administrator"
			notif.subject = subject
			notif.type = "Alert"
			notif.document_type = "Purchase Request"
			notif.document_name = self.name
			notif.insert(ignore_permissions=True)
		except Exception as e:
			frappe.log_error(title="Notification Error", message=str(e))

	def notify_roles(self, roles, subject):
		"""Send persistent alert to all Users with given role."""
		for role in roles:
			users = frappe.get_all("Has Role", filters={"role": role, "parenttype": "User"}, pluck="parent")
			for user in set(users):
				self.notify_user(user, subject)
