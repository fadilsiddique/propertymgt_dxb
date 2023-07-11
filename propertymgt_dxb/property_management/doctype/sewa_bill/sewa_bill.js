// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('SEWA Bill', {
	refresh: function(frm) {

		frm.add_custom_button(__('Room Bill'),function(){
			frappe.route_options={'sewa_bill':frm.doc.name}
			frappe.set_route('Form','Room Bill', 'new-room-bill')
		}, __('Create'))
	},

	sewa_amount:function(frm){
		let total_sewa_amount = frm.doc.sewa_amount + frm.doc.online_charges

		frm.set_value('total_sewa_amount', total_sewa_amount)
	},

	previous_electricity_reading:function(frm){
		let current_electricity_reading = frm.doc.current_electricity_reading
		let previous_electricity_reading = frm.doc.previous_electricity_reading
		let units_used = current_electricity_reading - previous_electricity_reading
		let electricity_amount = frm.doc.total_sewa_amount - (frm.doc.gas_amount + frm.doc.water_amount)
		frm.set_value({
			total_units_used: units_used,
			electricity_amount: electricity_amount
		})

		// frm.set_value('electricity_amount',units_used * frm.doc.electricity_rateunit)
	}
});
