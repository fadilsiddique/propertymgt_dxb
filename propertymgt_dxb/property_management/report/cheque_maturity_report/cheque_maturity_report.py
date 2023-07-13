# Copyright (c) 2023, HyperCloud and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns = [
        {"label": "Party Type", "fieldname": "party_type", "fieldtype": "Data", "width": 120},
        {"label": "Party", "fieldname": "party", "fieldtype": "Data", "width": 150},
        {"label": "Reference Date", "fieldname": "reference_date", "fieldtype": "Date", "width": 120},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120}
    ]

    filters = {
        "mode_of_payment": "Cheque",
        "reference_date": ["<=", frappe.utils.add_days(frappe.utils.nowdate(), 4)]
    }

    data = frappe.get_all("Payment Entry", fields=["party_type", "party", "reference_date", "posting_date"],
                          filters=filters)

    return columns, data



