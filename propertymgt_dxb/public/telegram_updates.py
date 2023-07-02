import frappe
import requests

@frappe.whitelist()
def getUpdate():

    settings = frappe.get_doc('Telegram Settings','Telegram Settings')
    token = settings.get_password(fieldname='token')
    url = 'https://api.telegram.org/bot{0}/getUpdates'.format(token)
    mobile_number = '',
    chat_id = '',
    username = '',
    json_data = ''
    message_json=requests.get(url).json()

    for result in message_json.result:
        
        doc = frappe.get_doc({
        'doctype':'Telegram Notification',
        'mobile_number':'',
        'chat_id':result['message']['chat']['id'],
        'username':'',
        'json_data':''
    })
        doc.insert(ignore_permsissions=True)
        doc.save(ignore_permsissions=True)





