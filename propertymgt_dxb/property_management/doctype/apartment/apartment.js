// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Apartment', {
	refresh: function(frm) {

		frm.add_custom_button(__('Flat'),function(){
			frappe.route_options={'apartment':frm.doc.name,}
			frappe.set_route('Form','Flat', 'new-flat')
		}, __('Create'))

	}
});
