# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Flat(Document):

	def after_insert(self):

		new_cost_center = frappe.get_doc({
			'doctype':'Cost Center',
			'cost_center_name':self.name,
			'parent_cost_center':self.apartment+' - ARE',
			'company':'Anjillam Real Estate',
		})

		new_cost_center.insert(ignore_permissions=True)
		new_cost_center.save(ignore_permissions=True)

		frappe.db.set_value('Flat',self.name,'cost_center',new_cost_center.name)
