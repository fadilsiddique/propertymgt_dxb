import frappe

@frappe.whitelist()
def append_customer_in_room(doc,event):

    room = frappe.get_doc('Room',doc.room)

    room.append("tenants",{
        "customer":doc.name
    })

    room.save()

def send_invoice(doc,event):
    customer = frappe.get_doc('Customer',doc.customer)