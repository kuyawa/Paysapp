from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello'

@app.route('/test', methods=['GET'])
def test():
    return 'Test'
    
@app.route('/bot', methods=['POST'])
def bot():
    txt = request.values.get('Body', '').lower()
    res = MessagingResponse()
    msg = res.message()
    ok  = False

    if 'hello' in txt:
        # Register phone
        text = 'Welcome to Paysapp'
        msg.body(text)
        ok = True

    if 'balance' in txt:
        # return balance in default currency
        #r = requests.get('https://api.example.com/balance/PHONEID/USD')
        #if r.status_code == 200:
        #    data = r.json()
        #    quote = '{"balance": 125.00}'
        #else:
        #    quote = 'Balance unavailable, try again in a minute'
        text = 'Your balance is 125.00 USD'
        msg.body(text)
        ok = True

    if 'pay' in txt:
        # split parts, verify info and send money
        # msg.media('https://gateway.example.com/receipt')
        text = 'Payment sent'
        msg.body(text)
        ok = True

    if not ok:
        msg.body('Invalid action, RTFM!')

    return str(res)

#print("Server running...")
#END