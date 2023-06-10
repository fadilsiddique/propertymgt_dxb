// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Flat', {
	refresh: function(frm) {

		frm.add_custom_button(__('Room'),function(){
			frappe.route_options={'apartment':frm.doc.apartment,'flat_no':frm.doc.name}
			frappe.set_route('Form','Room', 'new-room')
		}, __('Create'))
	}
});

