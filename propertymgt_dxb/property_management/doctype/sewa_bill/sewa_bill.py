# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from propertymgt_dxb.property_management.api.rental import calculate_days

class SEWABill(Document):
	def on_submit(self):
		customer = frappe.db.get_list('Customer',filters={
			'current_status':['In','Vacation'],
			'apartment':self.apartment,
			'flat':self.flat,
		},fields=['name','apartment','flat','room'])

		rooms_array = []

		for i in customer:
			room_object = {'customer':i['name'],'room':i['room']}
			rooms_array.append(room_object)

		room_occupancy_tracker = frappe.get_doc({
			'doctype':'Room Occupancy Tracker',
			'apartment':self.apartment,
			'flat':self.flat,
			'sewa_from':self.sewa_from,
			'sewa_to':self.sewa_to,
			'customers':rooms_array
		})

		room_occupancy_tracker.save(ignore_permissions=True)
		room_occupancy_tracker.submit()