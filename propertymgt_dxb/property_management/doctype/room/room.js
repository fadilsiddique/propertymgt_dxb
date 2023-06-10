// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room', {
	// refresh: function(frm) {

	// }

	apartment: function(frm){
		let apartment = frm.doc.apartment

		frm.set_query("flat_no",function(){
			return {
				filters:{
					'apartment':apartment
				}
			}
		})
	}
});
