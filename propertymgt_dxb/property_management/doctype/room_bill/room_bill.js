// Copyright (c) 2023, HyperCloud and contributors
// For license information, please see license.txt

frappe.ui.form.on('Room Bill', {
	refresh: function(frm) {

		frm.add_custom_button(__('Sales Invoice'),function(){

			frappe.call({
				method:'propertymgt_dxb.property_management.api.rental.make_sales_invoice',
				args:{
					apartment:frm.doc.apartment,
					flat:frm.doc.flat_no,
					sewa:frm.doc.customers,
					electricity:frm.doc.electricity_bill_table,
					gas:frm.doc.gas_bill_table,
					water:frm.doc.water_bill_table,
					internet:frm.doc.internet_bill_table,
					reference:frm.doc.name ? frm.doc.name : ''

				},
				callback:((response)=>{
					console.log(response)
				})
			})
		
			frappe.set_route('List','Sales Invoice','List')
		}, __('Create'))

	},
	apartment: function(frm){
		let apartment = frm.doc.apartment

		frm.set_query("flat_no",function(){
			return {
				filters:{
					'apartment':apartment
				}
			}
		})
	},

	flat_no: function(frm){
		
		let flat_number=frm.doc.flat_no
		let apartment = frm.doc.apartment

		frm.set_query("room_no",function(){
			return {
				filters:{
					'flat_no':flat_number,
					'apartment':apartment
				}
			}
		})
		
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

						let electricity_bill_table = frm.add_child('electricity_bill_table',{
							customer:e
						})
						let water_bill_table = frm.add_child('water_bill_table',{
							customer:e
						})
						let gas_bill_table = frm.add_child('gas_bill_table',{
							customer:e
						})
						let internet_bill_table = frm.add_child('internet_bill_table',{
							customer:e
						})
					})

				}
				frm.refresh_field('customers')
				frm.refresh_field('electricity_bill_table')
				frm.refresh_field('water_bill_table')
				frm.refresh_field('gas_bill_table')
				frm.refresh_field('internet_bill_table')
				

			})
		})

	},
	sewa_amount: function(frm){
		let customers = frm.doc.customers
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to = frm.doc.sewa_bill_to
		let sewa_amount = frm.doc.sewa_amount
		let customers_array = []

		console.log(customers)

		// customers.map((res)=>{
		// 	customers_array.push(res.customer)
		// })

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:customers,
				sewa_bill_from:sewa_bill_from,
				sewa_bill_to:sewa_bill_to,
				amount:sewa_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
				console.log(response)
				let res = response.message[0]
				frm.set_value('total_days_of_occupancy',response.message[1])
				const rate = frm.doc.sewa_amount/frm.doc.total_days_of_occupancy
				res.map((e)=>{
					var customers_child = frm.doc.customers
					for (var i = 0; i < customers_child.length; i++){
						var row = customers_child[i]
						if(e.customer == row.customer){
							frappe.model.set_value(row.doctype,row.name,'days',e.days)
							frappe.model.set_value(row.doctype,row.name,'rate',rate)

							let amount = row.rate * row.days
							frappe.model.set_value(row.doctype,row.name,'amount',amount)
							
						}
						
					}
				})

			}),

		})
		
	},
	electricity_amount: function(frm){
		let customers = frm.doc.electricity_bill_table
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to = frm.doc.sewa_bill_to
		let electricity_amount = frm.doc.electricity_amount
		let customers_array = []

		// customers.map((res)=>{
		// 	customers_array.push(res.customer)
		// })

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:customers,
				sewa_bill_from:sewa_bill_from,
				sewa_bill_to:sewa_bill_to,
				amount:electricity_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
				console.log(response)
				let res = response.message[0]
				frm.set_value('total_days_of_occupancy',response.message[1])
				const rate = frm.doc.electricity_amount/frm.doc.total_days_of_occupancy
				res.map((e)=>{
					var customers_child = frm.doc.electricity_bill_table
					for (var i = 0; i < customers_child.length; i++){
						var row = customers_child[i]
						if(e.customer == row.customer){
							frappe.model.set_value(row.doctype,row.name,'days',e.days)
							frappe.model.set_value(row.doctype,row.name,'rate',rate)

							let amount = row.rate * row.days
							frappe.model.set_value(row.doctype,row.name,'amount',amount)
							
						}
						
					}
				})

			
			}),

		})
		
	},
	water_amount: function(frm){
		let customers = frm.doc.water_bill_table
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to = frm.doc.sewa_bill_to
		let water_amount = frm.doc.water_amount
		let customers_array = []

		// customers.map((res)=>{
		// 	customers_array.push(res.customer)
		// })

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:customers,
				sewa_bill_from:sewa_bill_from,
				sewa_bill_to:sewa_bill_to,
				amount:water_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
				console.log(response)
				let res = response.message[0]
				frm.set_value('total_days_of_occupancy',response.message[1])
				const rate = frm.doc.water_amount/frm.doc.total_days_of_occupancy
				res.map((e)=>{
					var customers_child = frm.doc.water_bill_table
					for (var i = 0; i < customers_child.length; i++){
						var row = customers_child[i]
						if(e.customer == row.customer){
							frappe.model.set_value(row.doctype,row.name,'days',e.days)
							frappe.model.set_value(row.doctype,row.name,'rate',rate)

							let amount = row.rate * row.days
							frappe.model.set_value(row.doctype,row.name,'amount',amount)
							
						}
						
					}
				})

			
			}),

		})
		
	},
	gas_amount: function(frm){
		let customers = frm.doc.gas_bill_table
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to=frm.doc.sewa_bill_to
		let gas_amount = frm.doc.gas_amount
		let customers_array = []

		// customers.map((res)=>{
		// 	customers_array.push(res.customer)
		// })

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:customers,
				sewa_bill_from:sewa_bill_from,
				sewa_bill_to:sewa_bill_to,
				amount:gas_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
				console.log(response)
				let res = response.message[0]
				frm.set_value('total_days_of_occupancy',response.message[1])
				const rate = frm.doc.gas_amount/frm.doc.total_days_of_occupancy
				res.map((e)=>{
					var customers_child = frm.doc.gas_bill_table
					for (var i = 0; i < customers_child.length; i++){
						var row = customers_child[i]
						if(e.customer == row.customer){
							frappe.model.set_value(row.doctype,row.name,'days',e.days)
							frappe.model.set_value(row.doctype,row.name,'rate',rate)

							let amount = row.rate * row.days
							frappe.model.set_value(row.doctype,row.name,'amount',amount)
							
						}
						
					}
				})

			
			}),

		})
	},

	internet_amount: function(frm){
		let customers = frm.doc.internet_bill_table
		let amount = frm.doc.internet_amount
		let rate = amount/customers.length

		for (var i = 0; i < customers.length; i++){
			var row = customers[i]
			frappe.model.set_value(row.doctype,row.name,'rate',rate)
			frappe.model.set_value(row.doctype,row.name,'amount',rate)
		}

	}
});



// frappe.ui.form.on('Customers', {
// 	// refresh: function(frm) {

// 	// }
// }); 