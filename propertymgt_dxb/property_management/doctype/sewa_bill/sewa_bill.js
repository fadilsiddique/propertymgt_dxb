// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('SEWA Bill', {
	// refresh: function(frm) {

	// }

	previous_electricity_reading:function(frm){
		let current_electricity_reading = frm.doc.current_electricity_reading
		let previous_electricity_reading = frm.doc.previous_electricity_reading
		let units_used = current_electricity_reading - previous_electricity_reading
		frm.set_value('total_units_used',units_used)
		// frm.set_value('electricity_amount',units_used * frm.doc.electricity_rateunit)
	}
});
