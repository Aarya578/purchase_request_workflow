// Copyright (c) 2026, arise and contributors
// For license information, please see license.txt

// 1. Listen to events on the child table rows ("Purchase Request Item")
frappe.ui.form.on('Purchase Request Item', {
	qty: function(frm, cdt, cdn) {
		calculate_line_and_total(frm, cdt, cdn);
	},
	estimated_rate: function(frm, cdt, cdn) {
		calculate_line_and_total(frm, cdt, cdn);
	},
	items_remove: function(frm) {
		calculate_grand_total(frm);
	}
});

// Helper function: Calculate Line Amount (qty * rate)
function calculate_line_and_total(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let line_total = (row.qty || 0) * (row.estimated_rate || 0);

	frappe.model.set_value(cdt, cdn, 'estimated_amount', line_total);
	calculate_grand_total(frm);
}

// Helper function: Sum all line amounts into Estimated Total
function calculate_grand_total(frm) {
	let grand_total = 0;
	(frm.doc.items || []).forEach(row => {
		grand_total += (row.estimated_amount || 0);
	});
	frm.set_value('estimated_total', grand_total);
}