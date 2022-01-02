import midtransclient
from datetime import datetime
import json
import requests
# Function to clean ticket check in time string
def totally_clean_text(text):
 cleaned_text = text.strip("\'")
 return cleaned_text
# Function for cleaning our json
def clean_response(our_json):
 strs = our_json.replace("'", '"')
 clean = json.loads(strs.replace('u"', '"'))
 return clean
# Calling Midtrans API
def create_payment(ticket_id, total_payment):
 # Create timestamp
 timestamp = datetime.now().strftime("%Y-%m-%d 
%H:%M:%S")
 # Create Core API Instance
 core_api = midtransclient.CoreApi(
 is_production=False, 
 server_key='SB-Mid-server-bHLfTtkUR2dLONFY4PZBN2f_',
client_key='SB-Mid-client-f80B_P7CiZGfVSKI' 
 )
 # Build APi parameter
 param = {
 "payment_type": "gopay",
 "transaction_details": {
 "gross_amount": total_payment,
 "order_id": "park-id-"+timestamp
 },
 "gopay": {
 "enable_callback": True,
 "callback_url": "",
 }
 }
 # Charge transaction
 charge_response = core_api.charge(param)
 return charge_response
# Json response example
json_example = '''
{
 "status_code":"201",
 "status_message":"GoPay transaction is created",
 "transaction_id":"fa52a039-8f76-4184-8128-
5244d06bb723",
 "order_id":"park-id2021-07-02 15:03:01",
 "merchant_id":"G320883475",
 "gross_amount":"12145.00",
 "currency":"IDR",
"payment_type":"gopay",
 "transaction_time":"2021-07-02 15:03:51",
 "transaction_status":"pending",
 "fraud_status":"accept",
 "actions":[
 {
 "name":"generate-qr-code",
 "method":"GET",
 
"url":"https://api.sandbox.veritrans.co.id/v2/gopay/fa5
2a039-8f76-4184-8128-5244d06bb723/qr-code"
 },
 {
 "name":"deeplink-redirect",
 "method":"GET",
 
"url":"https://simulator.sandbox.midtrans.com/gopay/par
tner/app/payment-pin?id=2370139c-aecb-4086-8df1-
0fb31814d5e9"
 },
 {
 "name":"get-status",
 "method":"GET",
 
"url":"https://api.sandbox.veritrans.co.id/v2/fa52a039-
8f76-4184-8128-5244d06bb723/status"
 },
 {
 "name":"cancel",
 "method":"POST",
 
"url":"https://api.sandbox.veritrans.co.id/v2/fa52a039-
8f76-4184-8128-5244d06bb723/cancel"
}
 ]
}
'''
# Ectract qr code link
def create_qr_link(response):
 as_str = str(response)
 res= clean_response(as_str)
 qr_link = res['actions'][0]['url']
 print(qr_link)
 return qr_link
# Extract Transaction ID
def get_trx_id(response):
 as_str = str(response)
 res = clean_response(as_str)
 trx_id_got = res['transaction_id']
 print(trx_id_got)
 return trx_id_got
# Extract Order ID
def get_order_id(response):
 as_str = str(response)
 res = clean_response(as_str)
 order_id_got = res['order_id']
 return order_id_got
# Midtrans Get Payment Status
def get_status(order_id):
 headers = {
'Accept': 'application/json',
 'Content-Type': 'application/json',
 'Authorization': 'Basic 
U0ItTWlkLXNlcnZlci1iSExmVHRrVVIyZExPTkZZNFBaQk4yZl86'
 }
 response = 
requests.get('https://api.sandbox.midtrans.com/v2/' + 
order_id + '/status', headers=headers)
 print(response.text)
 return response.status_code