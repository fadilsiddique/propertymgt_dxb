// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Bill', {
	// refresh: function(frm) {

	// }

	flat_no: function(frm){
		
		let flat_number=frm.doc.flat_no
		
		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.get_customers_by_flat",
			args:{
				flat_no:flat_number
			},
			callback:((response)=>{
				let customers = response.message

				if (customers){

					customers.map((e)=>{
						let row =frm.add_child('customers',{
							customer:e,
						})
					})

				}
				frm.refresh_field('customers')
				

			})
		})

	},
	sewa_amount: function(frm){
		let customers = frm.doc.customers
		let sewa_date = frm.doc.sewa_bill_date
		let sewa_amount = frm.doc.sewa_amount
		let customers_array = []

		// customers.map((res)=>{
		// 	customers_array.push(res.customer)
		// })

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:customers,
				sewa_date:sewa_date,
				amount:sewa_amount
			},
			callback:((response)=>{
				console.log(response)
				let res = response.message[0]
				res.map((e)=>{
					var customers_child = frm.doc.customers
					for (var i = 0; i < customers_child.length; i++){
						var row = customers_child[i]
						if(e.customer == row.customer){
							frappe.model.set_value(row.doctype,row.name,'days',e.days)
						}
						
					}
				})

				frm.set_value('total_days_of_occupancy',response.message[1])

				const rate = frm.doc.sewa_amount/frm.doc.total_days_of_occupancy
				var customers_child = frm.doc.customers
				for (var i = 0; i < customers_child.length; i++){
					var row = customers_child[i]
						frappe.model.set_value(row.doctype,row.name,'rate',rate)
				}
				
				
			})
		})
		
	}

});



// frappe.ui.form.on('Customers', {
// 	// refresh: function(frm) {

// 	// }
// }); 