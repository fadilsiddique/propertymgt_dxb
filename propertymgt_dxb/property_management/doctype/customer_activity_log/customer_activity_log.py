# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CustomerActivityLog(Document):
	def on_submit(self):
		if self.activity_type == 'In' or self.activity_type == 'Out':
			frappe.db.set_value('Customer',self.customer,'current_status',self.activity_type)
		if self.activity_type == 'Out':
			room = frappe.get_doc('Room',self.room_no)
			
			for customer in room.tenants:
				if customer.customer ==self.customer:
					room.tenants.remove(customer)
			room.save()
