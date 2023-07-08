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
					electricity:frm.doc.electricity_usage_table,
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
	validate: function(frm){
		let sewa_amount = frm.doc.sewa_amount
		let water_amount = frm.doc.water_amount
		let gas_amount = frm.doc.gas_amount
		let electricity_amount = frm.doc.electricity_amount

		let municipality_charges = sewa_amount - (water_amount + gas_amount + electricity_amount)

		frm.set_value('sharjah_municipality_charges',municipality_charges)
	},
	sewa_bill: function(frm){

		frappe.db.get_doc('SEWA Bill',frm.doc.sewa_bill).then(doc =>{
			frm.set_value('sewa_amount',doc.sewa_amount)
			frm.set_value('water_amount',doc.water_amount)
			frm.set_value('gas_amount',doc.gas_amount)
			frm.set_value('electricity_amount',doc.electricity_amount)
			frm.set_value('previous_electricity_reading',doc.previous_electricity_reading)
			frm.set_value('current_electricity_reading',doc.current_electricity_reading)
			// frm.set_value('electricity_amount',doc.previous_electricity_reading + doc.current_electricity_reading)
			frm.set_value('total_units_used',doc.total_units_used)

		})
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
		let sewa_from=frm.doc.sewa_bill_from
		let sewa_to = frm.doc.sewa_bill_to
		console.log(sewa_from,"helllellel")

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
				flat_no:flat_number,
				sewa_from:sewa_from,				
				sewa_to:sewa_to
			},
			callback:((response)=>{
				let customers = response.message
				console.log(customers,"workkk")

				console.log(response.message)

				if (customers){
					frm.doc.customers = frm.doc.customers || [];
					customers.map((e)=>{
						console.log(e,"E")
						let existingCustomer = frm.doc.customers.find((customer) => customer.customer === e);
						if (!existingCustomer){
						frappe.db.get_list('Customer',{filters:{'name':e},fields:['name','room']})
						.then(function(event){
							let room = event[0]['room']
							let electricity_bill_table = frm.add_child('electricity_usage_table',{
								customer:e,
								room:room
							})

							frm.refresh_field('electricity_usage_table')
						})
						let row =frm.add_child('customers',{
							customer:e,
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
						}
					})

				}
				frm.refresh_field('customers')
				frm.refresh_field('electricity_usage_table')
				frm.refresh_field('water_bill_table')
				frm.refresh_field('gas_bill_table')
				frm.refresh_field('internet_bill_table')
				

			})
		})

		frappe.db.get_list('Room',{filters:
			{'flat_no':frm.doc.flat_no}})
			.then((e)=>{
			frm.doc.room_wise_ac_usage = frm.doc.room_wise_ac_usage || []
			e.map((res)=>{
				let existing_room = frm.doc.room_wise_ac_usage.find((room)=> room.room === res.name);
				if (!existing_room){
				let ac_usage_table = frm.add_child('room_wise_ac_usage',{
					room:res.name
				})
			}
			})
			frm.refresh_field('room_wise_ac_usage')
		})

	},
	sewa_amount: function(frm){
		let customers = frm.doc.customers
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to = frm.doc.sewa_bill_to
		let sewa_amount = frm.doc.sewa_amount
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
				amount:sewa_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
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
		let customers = frm.doc.electricity_usage_table
		let sewa_bill_from = frm.doc.sewa_bill_from
		let sewa_bill_to = frm.doc.sewa_bill_to
		let electricity_amount = frm.doc.electricity_amount

		frappe.call({
			method:"propertymgt_dxb.property_management.api.rental.calculate_days",
			args:{
				customers:frm.doc.electricity_usage_table,
				sewa_bill_from:sewa_bill_from,
				sewa_bill_to:sewa_bill_to,
				amount:electricity_amount,
				apartment:frm.doc.apartment,
				flat:frm.doc.flat_no
			},
			callback:((response)=>{
				let res = response.message[0]
				const rate = frm.doc.electricity_amount/frm.doc.total_days_of_occupancy
				res.map((e)=>{
					var customers_child = frm.doc.electricity_usage_table
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

	},
	total_electricity_amount_without_ac: function(frm){

		let rate_without_ac = (frm.doc.total_electricity_amount_without_ac/frm.doc.total_days_of_occupancy)
		let electricity_table = frm.doc.electricity_usage_table
		

		for (var i = 0; i < electricity_table.length; i++){
			var row = electricity_table[i]
			let ac_usage_table = frm.doc.room_wise_ac_usage
			frappe.model.set_value(row.doctype,row.name,'rate_w0_ac',rate_without_ac)
			
			let amount_without_ac = row.rate_w0_ac * row.days
			frappe.model.set_value(row.doctype,row.name,'amount_wo_ac',amount_without_ac)

			ac_usage_table.map((event)=>{
				if (row.room == event.room){
					let ac_usage_rate = (event.amount/frm.doc.total_days_of_occupancy)
					let ac_usage_amount = (ac_usage_rate*row.days)
					frappe.model.set_value(row.doctype,row.name,'ac_usage_amount', ac_usage_amount)
					frappe.model.set_value(row.doctype,row.name,'total_with_ac',(row.amount_wo_ac + ac_usage_amount))			
				}
			})
		}
	},

});






frappe.ui.form.on('Room Electricity Usage', {
	// refresh: function(frm) {

	// }

	ac_usage: function(frm,cdt,cdn){
		let room = locals[cdt][cdn]
		let sum = 0
		let total_ac_unit = 0
		let amount = (room.ac_usage)*room.electricity_rateunit
		frappe.model.set_value(cdt,cdn, 'amount',amount)
		frm.doc.room_wise_ac_usage.map((e)=>{
			sum += e.amount
			total_ac_unit += e.ac_usage
		})
		let amount_without_ac = frm.doc.total_electricity_amount_without_ac
		let total_electricity_amount = frm.doc.electricity_amount
		let total_units = frm.doc.total_units_used 

		frm.set_value('total_electricity_amount_without_ac',(total_electricity_amount - sum))
		frm.set_value('balance_units',total_units - total_ac_unit)

	}
}); 




