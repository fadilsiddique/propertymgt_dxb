# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from propertymgt_dxb.public.telegram_updates import sendMessage
from frappe.utils import get_files_path
from frappe.utils.file_manager import save_file, get_file_url
import base64


class RoomBill(Document):
	
	def on_submit(self):

		pdf_data = frappe.get_print(self.doctype,self.name, print_format = 'Room Bill', as_pdf=True)
		# pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')
		# pdf_file_path = get_files_path(f"Room Bill/{self.name}.pdf", is_private=0)
		file_id=save_file(f"{self.name}.pdf",pdf_data,self.doctype,self.name,"Home/Attachments/Room Bill",is_private=0)


		# document_path = f"/files/{self.name}.pdf"
		direct_url = get_file_url(file_id.name)
		message = f"Attached the flat bill of {self.flat_no}"

		frappe.enqueue(sendMessage,queue="short", message=message,document_path=direct_url)

		# sendMessage(message=message,document_path=direct_url)
