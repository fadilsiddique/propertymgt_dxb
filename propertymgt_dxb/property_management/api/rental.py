import frappe
from datetime import datetime
import json
import ast

@frappe.whitelist()
def get_customers_by_flat(flat_no):

    room_numbers=[]
    customers = []
    flat = frappe.get_doc('Flat',flat_no)
    rooms = flat.rooms

    for room in rooms:
        room_no = room.room_no
        room_numbers.append(room_no)

    for room_number in room_numbers:
        get_room = frappe.get_doc('Room',room_number)
        
        for tenant in get_room.tenants:
            customers.append(tenant.customer)

    return customers


@frappe.whitelist(allow_guest=True)
def calculate_days(customers,sewa_date,amount):

    tenant = ast.literal_eval(customers)
    sewa_date = sewa_date
    amount = amount

    data = []
    # customer123 = None

    for customer in tenant:
        # customer123 = customer123

        check_in_exist = frappe.db.exists("Customer Activity Log", {"customer": customer['customer'],'activity_type':'Check-In'})
        if check_in_exist:
            last_check_in= frappe.get_last_doc('Customer Activity Log',filters={"customer":customer['customer'],'activity_type':'Check-In'})
            last_check_in_date = str(last_check_in.check_in_date)
            sewa_date = str(sewa_date)
            date_format = "%Y-%m-%d"
            amount = amount

            start_date = datetime.strptime(last_check_in_date, date_format)
            end_date = datetime.strptime(sewa_date, date_format)

            num_days=(end_date - start_date).days

            data.append({
                'customer':customer['customer'],
                'days':num_days,
            })

    total_days = sum(item['days'] for item in data)


    return data, total_days






    

    
