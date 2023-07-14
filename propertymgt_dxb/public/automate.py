import frappe
from frappe.utils.file_manager import save_file, get_file_url
from propertymgt_dxb.public.telegram_updates import sendMessage

@frappe.whitelist()
def append_customer_in_room(doc,event):

    room = frappe.get_doc('Room',doc.room)

    room.append("tenants",{
        "customer":doc.name
    })

    room.save()

def send_invoice_via_telegram(doc,event):
		pdf_data = frappe.get_print(doc.doctype,doc.name, print_format = 'Standard', as_pdf=True)
		file_id=save_file(f"{doc.name}.pdf",pdf_data,doc.doctype,doc.name,"Home/Attachments/Sales Invoice",is_private=0)
		direct_url = get_file_url(file_id.name)
		message = f"Attached the room invoice of {doc.customer}"

		frappe.enqueue(sendMessage,queue="short", message=message,document_path=direct_url)