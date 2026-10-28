PURCHASE REQUESTWORKFLOW SYSTEM

Intern Project Specification

Technology: Frappe Framework / ERPNext

Project level: Intermediate  |  Suggested duration: 2–3 weeks

Prepared as a practical training brief for software development interns.

1. Project Overview

The Purchase Request Workflow System is a small business application that lets employees request items or services, routes requests to the appropriate manager for approval, and allows the purchasing team to track procurement through ordering and receipt. The application should provide clear status tracking, validation, role-based permissions, and an audit trail.

2. Problem Statement

Purchase requests are often raised through email, chat, or spreadsheets. This makes it difficult to know who approved a request, whether the budget was checked, what has been ordered, and whether the items have arrived. The system centralizes the process and makes each request traceable from submission to receipt.

3. Objectives

Create and submit purchase requests with item, quantity, estimated price, justification, and required-by date.

Route submitted requests to a manager for approval or rejection.

Allow purchasing staff to record supplier and order details after approval.

Track partial or complete receipt of ordered items.

Restrict actions based on user roles and current workflow state.

Provide dashboards, filters, and reports for request status and spending visibility.

Maintain comments and an activity history for important actions.

4. Scope

In scope

Employee request creation, editing while in Draft, submission, and status tracking.

Manager approval/rejection with a mandatory decision comment for rejection.

Purchasing team order entry, supplier details, and expected delivery date.

Goods receipt entry with received quantity and optional notes.

Role permissions, notifications, basic reports, and audit history.

Out of scope for the first version

Automatic payment processing, accounting integrations, and tax calculations.

Automatic supplier quotation comparison or purchase-order transmission to external systems.

Complex multi-currency budgeting and advanced approval matrices.

Production deployment or integration with a company ERP unless separately approved.

5. User Roles and Permissions

Role | Allowed actions | Restrictions

Role

Allowed actions

Restrictions

Employee / Requester | Create requests; edit own Draft requests; submit; view own requests; add permitted comments. | Cannot approve own request or mark an order as received.

Employee / Requester

Create requests; edit own Draft requests; submit; view own requests; add permitted comments.

Cannot approve own request or mark an order as received.

Manager / Approver | Review submitted requests; approve or reject; provide a decision comment. | Cannot edit request line items during approval; cannot approve a Draft request.

Manager / Approver

Review submitted requests; approve or reject; provide a decision comment.

Cannot edit request line items during approval; cannot approve a Draft request.

Purchasing Officer | View approved requests; record supplier/order details; update order status; record receipt quantities. | Cannot order a request that is not approved.

Purchasing Officer

View approved requests; record supplier/order details; update order status; record receipt quantities.

Cannot order a request that is not approved.

Administrator | Configure DocTypes, workflow, roles, notifications, and reports; troubleshoot records. | Administrative access should be limited to trusted users.

Administrator

Configure DocTypes, workflow, roles, notifications, and reports; troubleshoot records.

Administrative access should be limited to trusted users.

6. Workflow and Status Rules

Status | Owner / action | Allowed next step

Status

Owner / action

Allowed next step

Draft | Requester prepares the request and can edit details. | Submitted

Draft

Requester prepares the request and can edit details.

Submitted

Submitted | Request is locked for requester edits and waits for manager review. | Approved or Rejected

Submitted

Request is locked for requester edits and waits for manager review.

Approved or Rejected

Approved | Manager approval is recorded; purchasing may proceed. | Ordered

Approved

Manager approval is recorded; purchasing may proceed.

Ordered

Rejected | Manager records reason; requester can review and, if required, create a revised request. | Draft/re-submit via a controlled revision, or closed

Rejected

Manager records reason; requester can review and, if required, create a revised request.

Draft/re-submit via a controlled revision, or closed

Ordered | Purchasing records supplier, order reference, order date, and expected delivery. | Partially Received or Received

Ordered

Purchasing records supplier, order reference, order date, and expected delivery.

Partially Received or Received

Partially Received | Purchasing records a receipt less than the outstanding quantity. | Partially Received or Received

Partially Received

Purchasing records a receipt less than the outstanding quantity.

Partially Received or Received

Received | All requested quantities have been received and verified. | Closed / terminal

Received

All requested quantities have been received and verified.

Closed / terminal

Cancelled | An authorized user cancels before receipt, with a reason. | Terminal or admin-controlled reopen

Cancelled

An authorized user cancels before receipt, with a reason.

Terminal or admin-controlled reopen

Implementation note: The brief’s core path is Draft → Submitted → Approved → Ordered → Received. Rejected, Partially Received, and Cancelled are recommended supporting states so the system handles real cases. Use Frappe Workflow states and transition rules; do not rely on a free-text status field alone.

7. Functional Requirements

ID | Requirement | Acceptance description

ID

Requirement

Acceptance description

FR-01 | Create request | Requester can create a request with a title, department/cost centre, business justification, required-by date, and one or more line items.

FR-01

Create request

Requester can create a request with a title, department/cost centre, business justification, required-by date, and one or more line items.

FR-02 | Line-item details | Each line contains item/description, quantity, unit, estimated unit price, and calculated line total.

FR-02

Line-item details

Each line contains item/description, quantity, unit, estimated unit price, and calculated line total.

FR-03 | Validation | Require at least one line item, positive quantities, non-negative prices, a justification, and a valid required-by date.

FR-03

Validation

Require at least one line item, positive quantities, non-negative prices, a justification, and a valid required-by date.

FR-04 | Submit | Submission validates required fields and moves the document to Submitted; requester editing is then restricted.

FR-04

Submit

Submission validates required fields and moves the document to Submitted; requester editing is then restricted.

FR-05 | Approval | Manager can approve or reject; rejection requires a reason. The system records who acted and when.

FR-05

Approval

Manager can approve or reject; rejection requires a reason. The system records who acted and when.

FR-06 | Order tracking | Purchasing can enter supplier, purchase order/reference number, order date, expected delivery date, and ordered quantities.

FR-06

Order tracking

Purchasing can enter supplier, purchase order/reference number, order date, expected delivery date, and ordered quantities.

FR-07 | Receipt tracking | Purchasing can enter received quantities and notes; received quantity cannot exceed outstanding quantity unless an authorized override is implemented.

FR-07

Receipt tracking

Purchasing can enter received quantities and notes; received quantity cannot exceed outstanding quantity unless an authorized override is implemented.

FR-08 | Notifications | Notify the manager on submission, requester on decision, and requester/manager on receipt completion.

FR-08

Notifications

Notify the manager on submission, requester on decision, and requester/manager on receipt completion.

FR-09 | Audit history | Record status changes, decisions, order updates, receipt entries, user, timestamp, and comments.

FR-09

Audit history

Record status changes, decisions, order updates, receipt entries, user, timestamp, and comments.

FR-10 | Reports | Provide filters by status, requester, department, approver, supplier, and date range; show estimated total value.

FR-10

Reports

Provide filters by status, requester, department, approver, supplier, and date range; show estimated total value.

8. Suggested Data Model / DocTypes

DocType | Important fields | Notes

DocType

Important fields

Notes

Purchase Request | requester, department, cost_centre, justification, required_by, status/workflow_state, estimated_total, approver, decision_comment | Parent document. Use permissions and Workflow for lifecycle control.

Purchase Request

requester, department, cost_centre, justification, required_by, status/workflow_state, estimated_total, approver, decision_comment

Parent document. Use permissions and Workflow for lifecycle control.

Purchase Request Item | item_code or description, qty, uom, estimated_rate, estimated_amount, received_qty | Child table linked to Purchase Request. Calculate amount from qty × rate.

Purchase Request Item

item_code or description, qty, uom, estimated_rate, estimated_amount, received_qty

Child table linked to Purchase Request. Calculate amount from qty × rate.

Purchase Order Details | supplier, supplier_reference, order_date, expected_delivery_date, ordered_by | Can be fields on the parent for the first version; split into a DocType if multiple orders per request are needed.

Purchase Order Details

supplier, supplier_reference, order_date, expected_delivery_date, ordered_by

Can be fields on the parent for the first version; split into a DocType if multiple orders per request are needed.

Purchase Receipt Log | purchase_request, item_row/reference, received_qty, receipt_date, received_by, notes | Recommended separate child table or DocType to preserve multiple receipt events.

Purchase Receipt Log

purchase_request, item_row/reference, received_qty, receipt_date, received_by, notes

Recommended separate child table or DocType to preserve multiple receipt events.

Workflow / Activity history | document, previous_state, new_state, action_by, action_time, comment | Use Frappe workflow/audit facilities where suitable; avoid duplicating standard history without a reason.

Workflow / Activity history

document, previous_state, new_state, action_by, action_time, comment

Use Frappe workflow/audit facilities where suitable; avoid duplicating standard history without a reason.

9. Business Rules and Calculations

Line amount = quantity × estimated unit price.

Estimated total = sum of all line amounts.

Only the requester may edit a Draft request; submitted requests are read-only for the requester unless formally returned for revision.

Only an authorized approver can approve or reject a Submitted request.

Purchasing can start ordering only after approval.

Received quantity must be greater than zero and must not exceed the remaining ordered quantity.

A request becomes Received only when all required quantities have been received.

Rejection and cancellation must capture a reason.

Do not treat client-side field hiding as security. Enforce permissions and validations server-side.

10. Recommended Frappe Implementation

Create a custom app (for example, purchase_request_workflow) in a development site.

Create the Purchase Request DocType and its line-item child table.

Configure roles: Requester, Purchase Approver, Purchasing Officer, and Administrator.

Configure a Frappe Workflow with explicit states, allowed transitions, and role restrictions.

Implement server-side validation for quantities, dates, prices, status transitions, and receipt quantities.

Add notifications using Frappe Notification or an approved email mechanism.

Create list views, workspace/dashboard shortcuts, and reports for pending approvals, approved requests awaiting orders, and overdue deliveries.

Add test records for each role and each workflow transition before demonstrating the project.

11. Pages / Screens

Screen | Purpose

Screen

Purpose

My Purchase Requests | Requester sees own requests, statuses, totals, and required-by dates.

My Purchase Requests

Requester sees own requests, statuses, totals, and required-by dates.

New / Edit Request | Draft form with header details and line-item grid.

New / Edit Request

Draft form with header details and line-item grid.

Pending Approvals | Manager filters Submitted requests and opens each request for a decision.

Pending Approvals

Manager filters Submitted requests and opens each request for a decision.

Approved Requests to Order | Purchasing team identifies approved requests that do not yet have order details.

Approved Requests to Order

Purchasing team identifies approved requests that do not yet have order details.

Order Tracking | Shows supplier, order reference, expected delivery, and outstanding quantities.

Order Tracking

Shows supplier, order reference, expected delivery, and outstanding quantities.

Receipt Entry | Records one or more receipt events and updates the overall status.

Receipt Entry

Records one or more receipt events and updates the overall status.

Reports / Dashboard | Counts by status, estimated value by department, pending approvals, and overdue requests.

Reports / Dashboard

Counts by status, estimated value by department, pending approvals, and overdue requests.

12. Test Plan and Acceptance Criteria

Test case | Expected result

Test case

Expected result

Submit a valid request with one or more items. | Request moves from Draft to Submitted and appears in the manager’s queue.

Submit a valid request with one or more items.

Request moves from Draft to Submitted and appears in the manager’s queue.

Submit without justification or line items. | Submission is blocked with a clear validation message.

Submit without justification or line items.

Submission is blocked with a clear validation message.

Requester attempts to approve their own request. | Action is denied by permissions/workflow rules.

Requester attempts to approve their own request.

Action is denied by permissions/workflow rules.

Manager rejects without a reason. | Rejection is blocked until a reason is entered.

Manager rejects without a reason.

Rejection is blocked until a reason is entered.

Purchasing attempts to order a Submitted request. | Action is denied; only Approved requests can be ordered.

Purchasing attempts to order a Submitted request.

Action is denied; only Approved requests can be ordered.

Enter a negative quantity or price. | Validation rejects the value.

Enter a negative quantity or price.

Validation rejects the value.

Record a partial receipt. | Status becomes Partially Received and outstanding quantity is calculated correctly.

Record a partial receipt.

Status becomes Partially Received and outstanding quantity is calculated correctly.

Receive all remaining quantities. | Status becomes Received and the completion notification is sent.

Receive all remaining quantities.

Status becomes Received and the completion notification is sent.

Unauthorized user attempts to edit another user’s request. | Access is denied.

Unauthorized user attempts to edit another user’s request.

Access is denied.

Review request history. | Status changes and key actions show actor, time, and comments.

Review request history.

Status changes and key actions show actor, time, and comments.

13. Intern Task Breakdown

Phase | Tasks | Deliverable

Phase

Tasks

Deliverable

Phase 1 — Understand | Review requirements, draw workflow, identify roles and fields. | Workflow diagram and field list

Phase 1 — Understand

Review requirements, draw workflow, identify roles and fields.

Workflow diagram and field list

Phase 2 — Build data model | Create DocTypes, child table, field types, naming series, and list view. | Working request form

Phase 2 — Build data model

Create DocTypes, child table, field types, naming series, and list view.

Working request form

Phase 3 — Workflow and permissions | Configure states/transitions and role permissions; test allowed and denied actions. | Controlled approval flow

Phase 3 — Workflow and permissions

Configure states/transitions and role permissions; test allowed and denied actions.

Controlled approval flow

Phase 4 — Validation and notifications | Add server-side validations and notification rules. | Reliable business rules

Phase 4 — Validation and notifications

Add server-side validations and notification rules.

Reliable business rules

Phase 5 — Reports and testing | Build reports, run test cases, fix defects. | Test evidence and reports

Phase 5 — Reports and testing

Build reports, run test cases, fix defects.

Test evidence and reports

Phase 6 — Handover | Write setup instructions, known limitations, screenshots, and demo script. | README and demo

Phase 6 — Handover

Write setup instructions, known limitations, screenshots, and demo script.

README and demo

14. Suggested Timeline

Week | Target

Week

Target

Week 1 | Requirements, workflow diagram, DocTypes, forms, roles, and basic permissions.

Week 1

Requirements, workflow diagram, DocTypes, forms, roles, and basic permissions.

Week 2 | Approval transitions, server-side validation, notifications, and order/receipt tracking.

Week 2

Approval transitions, server-side validation, notifications, and order/receipt tracking.

Week 3 (buffer) | Reports, testing, bug fixes, documentation, and final demo.

Week 3 (buffer)

Reports, testing, bug fixes, documentation, and final demo.

Timeline assumes a single intern with access to a working Frappe development environment and regular mentor reviews.

15. Deliverables

Source code in a version-controlled repository.

Workflow diagram and DocType/field documentation.

Working Frappe app on a development site.

Role and permission matrix.

Test cases with pass/fail results and evidence.

README with installation/setup steps and known limitations.

Short demonstration covering a request from creation through receipt.

16. Evaluation Rubric

Area | Weight | What good looks like

Area

Weight

What good looks like

Workflow correctness | 25% | Only valid transitions are possible; rejection and receipt paths work.

Workflow correctness

25%

Only valid transitions are possible; rejection and receipt paths work.

Data model and validation | 20% | Fields are appropriate; calculations and server-side checks are reliable.

Data model and validation

20%

Fields are appropriate; calculations and server-side checks are reliable.

Permissions and security | 20% | Roles have least-privilege access; users cannot bypass approvals.

Permissions and security

20%

Roles have least-privilege access; users cannot bypass approvals.

Usability and reports | 15% | Forms are clear; filters and status visibility help each role.

Usability and reports

15%

Forms are clear; filters and status visibility help each role.

Testing | 10% | Positive, negative, and permission tests are documented.

Testing

10%

Positive, negative, and permission tests are documented.

Code quality and handover | 10% | Readable code, sensible naming, Git history, and clear setup instructions.

Code quality and handover

10%

Readable code, sensible naming, Git history, and clear setup instructions.

17. Questions for the Intern Demo

Why should the workflow be enforced server-side as well as represented in the UI?

How do you prevent a requester from approving their own request?

What happens when only part of an order is received?

How are estimated totals calculated and validated?

How would you support requests that require two levels of approval?

What information should be preserved in the audit trail?

18. Definition of Done

A requester can create and submit a valid purchase request.

A manager can approve or reject it with the required decision details.

Purchasing can record order information and one or more receipt events.

Status transitions, permissions, and validations are tested.

Reports show request status and estimated totals accurately.

The repository and README allow another developer to set up and review the project.