import frappe
import requests
import json


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

@frappe.whitelist()

def sendMessage(message,document_path):

    settings = frappe.get_doc('Telegram Settings','Telegram Settings')
    BOT_API_KEY = settings.get_password(fieldname='token')
    BASE_URL = settings.base_url
    message_response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
        'chat_id': settings.chat_id,
        'text': message
    })

    # document_files = {"document": open(document_path, "rb")}
    document_params = {"chat_id":1616214251,"document":f"{BASE_URL}{document_path}"}
    document_response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendDocument',params=document_params)

    if message_response.status_code == 200 and document_response.status_code == 200:
        frappe.publish_progress(25, title='Sending Document To Telegrm', description='Sending..')
    else:
        frappe.throw("Document Failed To Send")





