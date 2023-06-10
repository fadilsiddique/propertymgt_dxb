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
def calculate_days(customers,sewa_bill_from,sewa_bill_to,amount,apartment,flat):

    tenant = ast.literal_eval(customers)
    sewa_bill_from = sewa_bill_from
    sewa_bill_to=sewa_bill_to
    amount = amount

    data = []
    for customer in tenant:

        check_in_exist=frappe.db.exists(
            "Customer Activity Log",{
                'customer':customer['customer'],
                'activity_type':'Check-In',
                'apartment':apartment,
                'flat_no':flat,
                'check_in_date':['between',[sewa_bill_from,sewa_bill_to]]

            }
        )

        check_out_exist = frappe.db.exists(
            "Customer Activity Log",{
                'customer':customer['customer'],
                'activity_type':'Check-Out',
                'apartment':apartment,
                'flat_no':flat,
                'check_out_date':['between',[sewa_bill_from,sewa_bill_to]]

            }
        )

        vacation_exist = frappe.db.exists(
            "Customer Activity Log",{
                'customer':customer['customer'],
                'activity_type':'Vacation',
                'apartment':apartment,
                'flat_no':flat,
                'vacation_from':['between',[sewa_bill_from,sewa_bill_to]]

            }
        )

        if check_in_exist and not check_out_exist:
            check_in = frappe.get_doc(
                'Customer Activity Log',check_in_exist
            )

            check_in_date = str(check_in.check_in_date)
            sewa_bill_from = str(sewa_bill_from)
            sewa_bill_to = str(sewa_bill_to)
            date_format = "%Y-%m-%d"
            amount = amount
            start_date = datetime.strptime(check_in_date, date_format)
            end_date = datetime.strptime(sewa_bill_to, date_format)

            if vacation_exist:
                print(vacation_exist)
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_start_date = vacation.vacation_from
                vacation_end_date = vacation.to
                total_vacation_days = ((end_date-vacation_start_date).days) if vacation_end_date > end_date else(vacation_end_date - vacation_start_date).days 
                num_days=((end_date - start_date).days) - total_vacation_days

            else:
                num_days=(end_date - start_date).days

            data.append({
                'customer':customer['customer'],
                'days':num_days
            })

        elif check_in_exist and check_out_exist:
            check_in = frappe.get_doc(
                'Customer Activity Log',check_in_exist
            )

            check_out = frappe.get_doc(
                'Customer Activity Log', check_out_exist
            )

            check_in_date = str(check_in.check_in_date)
            check_out_date = str(check_out.check_out_date)
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(check_in_date, date_format)
            end_date = datetime.strptime(check_out_date, date_format)

            if vacation_exist:
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_start_date = vacation.vacation_from
                vacation_end_date = vacation.to
                total_vacation_days = (vacation_end_date - vacation_start_date).days
                num_days=((end_date - start_date).days) - total_vacation_days

            else:
                num_days=(end_date - start_date).days

            data.append({
                'customer':customer['customer'],
                'days':num_days
            })

        elif not check_in_exist and check_out_exist:
            check_out = frappe.get_doc(
                'Customer Activity Log',check_in_exist
            )
            check_out_date = str(check_out.check_out_date)
            sewa_bill_from = str(sewa_bill_from)
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(sewa_bill_from, date_format)
            end_date = datetime.strptime(check_out_date, date_format)

            if vacation_exist:
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_start_date = vacation.vacation_from
                vacation_end_date = vacation.to
                total_vacation_days = (vacation_end_date - vacation_start_date).days
                num_days=((end_date - start_date).days) - total_vacation_days

            else:
                num_days=(end_date - start_date).days

            data.append({
                'customer':customer['customer'],
                'days':num_days
            })

        elif not check_in_exist and not check_out_exist:
            sewa_bill_from = str(sewa_bill_from)
            sewa_bill_to = str(sewa_bill_to)
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(sewa_bill_from, date_format)
            end_date = datetime.strptime(sewa_bill_to, date_format)

            if vacation_exist:
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_start_date = vacation.vacation_from
                vacation_end_date = vacation.to
                total_vacation_days = (vacation_end_date - vacation_start_date).days
                num_days=((end_date - start_date).days) - total_vacation_days

            else:
                num_days=(end_date - start_date).days

            data.append({
                'customer':customer['customer'],
                'days':num_days
            })

    total_days = sum(item['days'] for item in data)

    return data, total_days