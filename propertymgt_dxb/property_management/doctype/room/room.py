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
