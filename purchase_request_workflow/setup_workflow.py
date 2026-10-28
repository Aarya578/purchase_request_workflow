import frappe

def create_workflow():
	# 1. Ensure all Workflow States exist
	states = [
		"Draft",
		"Submitted",
		"Approved",
		"Rejected",
		"Ordered",
		"Partially Received",
		"Received",
		"Cancelled"
	]
	for state in states:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc({
				"doctype": "Workflow State",
				"workflow_state_name": state
			}).insert(ignore_permissions=True)
			print(f"Created Workflow State: {state}")

	# 2. Ensure all Workflow Actions exist in 'Workflow Action Master'
	actions = [
		"Submit",
		"Approve",
		"Reject",
		"Revise",
		"Place Order",
		"Receive Partial",
		"Receive All",
		"Complete Receipt",
		"Cancel"
	]
	for action in actions:
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc({
				"doctype": "Workflow Action Master",
				"workflow_action_name": action
			}).insert(ignore_permissions=True)
			print(f"Created Workflow Action: {action}")

	# 3. Check if Workflow already exists
	workflow_name = "Purchase Request Approval Flow"
	if frappe.db.exists("Workflow", workflow_name):
		wf = frappe.get_doc("Workflow", workflow_name)
		wf.states = []
		wf.transitions = []
	else:
		wf = frappe.new_doc("Workflow")
		wf.workflow_name = workflow_name

	wf.document_type = "Purchase Request"
	wf.workflow_state_field = "workflow_state"
	wf.is_active = 1

	# 4. Add States Table
	# doc_status: 0 = Draft/Unsubmitted, 1 = Submitted/Active, 2 = Cancelled
	state_rows = [
		{"state": "Draft", "doc_status": "0", "allow_edit": "Purchase Requester"},
		{"state": "Submitted", "doc_status": "0", "allow_edit": "Purchase Approver"},
		{"state": "Approved", "doc_status": "1", "allow_edit": "Purchase Officer"},
		{"state": "Rejected", "doc_status": "0", "allow_edit": "Purchase Requester"},
		{"state": "Ordered", "doc_status": "1", "allow_edit": "Purchase Officer"},
		{"state": "Partially Received", "doc_status": "1", "allow_edit": "Purchase Officer"},
		{"state": "Received", "doc_status": "1", "allow_edit": "Purchase Officer"},
		{"state": "Cancelled", "doc_status": "2", "allow_edit": "System Manager"}
	]
	for row in state_rows:
		wf.append("states", row)

	# 5. Add Transitions Table
	# Note: In Frappe, transitioning to doc_status: 2 (Cancelled) requires current doc_status to be 1 (Submitted/Approved)
	transition_rows = [
		{"state": "Draft", "action": "Submit", "next_state": "Submitted", "allowed": "Purchase Requester"},
		{"state": "Submitted", "action": "Approve", "next_state": "Approved", "allowed": "Purchase Approver"},
		{"state": "Submitted", "action": "Reject", "next_state": "Rejected", "allowed": "Purchase Approver"},
		{"state": "Rejected", "action": "Revise", "next_state": "Draft", "allowed": "Purchase Requester"},
		{"state": "Approved", "action": "Place Order", "next_state": "Ordered", "allowed": "Purchase Officer"},
		{"state": "Approved", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
		{"state": "Ordered", "action": "Receive Partial", "next_state": "Partially Received", "allowed": "Purchase Officer"},
		{"state": "Ordered", "action": "Receive All", "next_state": "Received", "allowed": "Purchase Officer"},
		{"state": "Ordered", "action": "Cancel", "next_state": "Cancelled", "allowed": "System Manager"},
		{"state": "Partially Received", "action": "Complete Receipt", "next_state": "Received", "allowed": "Purchase Officer"}
	]
	for row in transition_rows:
		wf.append("transitions", row)

	wf.save(ignore_permissions=True)
	frappe.db.commit()
	print("Successfully created and activated 'Purchase Request Approval Flow'!")
