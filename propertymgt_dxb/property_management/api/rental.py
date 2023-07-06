import frappe
from datetime import datetime
import json
import ast

@frappe.whitelist()
def get_customers_by_flat(flat_no,sewa_from,sewa_to):

    room_numbers=[]
    customers = []
    date_format = "%Y-%m-%d"
    sewa_from = str(sewa_from)
    sewa_to = str(sewa_to)
    sewa_from_fromat = datetime.strptime(sewa_from, date_format)
    sewa_to_format = datetime.strptime(sewa_to,date_format)
    ##add filter staus=in
    tenants = frappe.db.get_list('Customer',filters={
        'flat':flat_no,
    },
    fields=['name','flat','current_status','last_checkout_date']
    )

    print(tenants),"tenanananna"
    for tenant in tenants:
        print(tenant.current_status)
        print(tenant.name)
        last_checkout_date = str(tenant.last_checkout_date)
        last_checkout_format=datetime.strptime(last_checkout_date,date_format)
        if tenant.current_status == 'Out' and sewa_from_fromat <= last_checkout_format <= sewa_to_format:
            
            customers.append(tenant.name)
            print(customers,"out")

        if tenant.current_satus == 'In' or tenant.current_satus ==' Vacation':

            customers.append(tenant.name)
            print(customers,"in")
    print(customers)
        
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
                'activity_type':'In',
                'apartment':apartment,
                'flat_no':flat,
                'check_in_date':['between',[sewa_bill_from,sewa_bill_to]]

            }
        )
        check_out_exist = frappe.db.exists(
            "Customer Activity Log",{
                'customer':customer['customer'],
                'activity_type':'Out',
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
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_from_date = str(vacation.vacation_from)
                vacation_to_date = str(vacation.to)
                vacation_start_date = datetime.strptime(vacation_from_date,date_format)
                vacation_end_date = datetime.strptime(vacation_to_date,date_format)
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
                vacation_from_date = str(vacation.vacation_from)
                vacation_to_date = str(vacation.to)
                vacation_start_date = datetime.strptime(vacation_from_date,date_format)
                vacation_end_date = datetime.strptime(vacation_to_date,date_format)
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
                'Customer Activity Log',check_out_exist
            )
            check_out_date = str(check_out.check_out_date)
            sewa_bill_from = str(sewa_bill_from)
            date_format = "%Y-%m-%d"
            start_date = datetime.strptime(sewa_bill_from, date_format)
            end_date = datetime.strptime(check_out_date, date_format) 

            if vacation_exist:
                ## if multiple vacation use frappe.db.get_list -> add vacations and reduce from num days
                vacation = frappe.get_doc('Customer Activity Log',vacation_exist)
                vacation_from_date = str(vacation.vacation_from)
                vacation_to_date = str(vacation.to)
                vacation_start_date = datetime.strptime(vacation_from_date,date_format)
                vacation_end_date = datetime.strptime(vacation_to_date,date_format)
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
                vacation_from_date = str(vacation.vacation_from)
                vacation_to_date = str(vacation.to)
                vacation_start_date = datetime.strptime(vacation_from_date,date_format)
                vacation_end_date = datetime.strptime(vacation_to_date,date_format)
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
#TO DO -> put invoicing function in que for better perfomance

# def invoice_queue(apartment,flat,sewa,electricity,gas,water,internet,reference):
#     frappe.enqueue(
#         make_sales_invoice,
#         queue='default',
#         apartment=apartment,
#         flat=flat,
#         sewa=sewa,
#         electricity=electricity,
#         gas=gas,
#         water=water,
#         internet=internet,reference=reference
#     )
@frappe.whitelist()
def make_sales_invoice(apartment,flat,sewa,electricity,gas,water,internet,reference):

    customers= ast.literal_eval(sewa)
    electricity=ast.literal_eval(electricity)
    gas=ast.literal_eval(gas)
    water=ast.literal_eval(water)
    internet=ast.literal_eval(internet)
    tenants =[]

    for customer in customers:
        tenants.append(customer['customer'])

    for tenant in tenants:

        customer = frappe.get_doc('Customer',tenant)
        rate= customer.rent_amount

        filtered_electricity = [item for item in electricity if item['customer'] == tenant]
        filtered_water = [item for item in water if item['customer'] == tenant]
        filtered_gas = [item for item in gas if item['customer'] == tenant]
        filtered_internet = [item for item in internet if item['customer'] == tenant]


        total_electricity = 0
        total_water = 0
        total_gas = 0 
        total_internet =0

        for item in filtered_electricity:
            total_electricity +=float(item['total_with_ac'])
        
        for item in filtered_gas:
            total_gas +=item['amount']

        for item in filtered_water:
            total_water += item['amount']
        for item in filtered_internet:
            total_internet +=item['amount']


        new_invoice = frappe.get_doc({
            'doctype': 'Sales Invoice',
            'customer':tenant,
            'room_bill_reference_id':reference if reference else "",
            'items':[
                {
                    'item_code':customer.service_type,
                    'rate':rate,
                    'qty':1
                },
                {
                    'item_code':'ELECTRICITY',
                    'rate':total_electricity,
                    'qty':1

                },
                {
                    'item_code':'WATER',
                    'rate':total_water,
                    'qty':1

                },
                {
                    'item_code':'GAS',
                    'rate':total_gas,
                    'qty':1

                },
                {
                    'item_code':'DATA',
                    'rate':total_internet,
                    'qty':1
                },
            ]
        })

        new_invoice.insert(ignore_permissions=True)

@frappe.whitelist()
def make_room_bill(
    apartment=None,
    flat=None,
    sewa_amount=None,
    water_amount=None,
    electricity_amount=None,
    gas_amount=None
):
    room_bill = frappe.get_doc({
        'doctype':'Room Bill',
        'apartment':apartment,
        'flat_no':flat,
        'sewa_amount':sewa_amount,
        'water_amount':water_amount,
        'electricity_amount':electricity_amount,
        'gas_amount':gas_amount
    })

    room_bill.insert(ignore_permissions=True)
    room_bill.save(ignore_permissions=True)



    