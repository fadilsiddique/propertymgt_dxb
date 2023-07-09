# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Room(Document):
	def after_insert(self):
		flat = frappe.get_doc('Flat',self.flat_no)

		flat.append("rooms",{
			"room_no":self.name
		})
		flat.save()

	def on_update(self):

		total_no_of_tenants = len(self.tenants)
		frappe.db.set_value(self.doctype,self.name,'total_no_of_tenants',total_no_of_tenants)

		print(total_no_of_tenants,"total tenan")

		if self.capacity:
			print(type(self.capacity))
			available_bed_space = int(self.capacity) - total_no_of_tenants
			frappe.db.set_value(self.doctype,self.name,'available_bed_space',str(available_bed_space))

