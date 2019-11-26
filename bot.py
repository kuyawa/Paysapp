import os
import requests
from flask import Flask, request, current_app, abort
from functools import wraps
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Environment variables

TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
GATEWAY = os.environ.get('GATEWAY')
APP_DEBUG = (TWILIO_AUTH_TOKEN is None)


# Twilio validation
def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(TWILIO_AUTH_TOKEN)

        # Validate the request using its URL, POST data and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if it's not
        if request_valid or current_app.debug:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


# Routing

@app.route('/', methods=['GET'])
def index():
    return 'Hello'


@app.route('/test', methods=['GET'])
def test():
    return 'Test'


@app.route('/bot', methods=['POST'])
@validate_twilio_request
def bot():
    txt = request.values.get('Body', '').lower()
    res = MessagingResponse()
    ok  = False
    
    if not GATEWAY: 
        text = 'Paysapp is down. Try again later'
        res.message(text)
        return str(res)


    if 'hello' in txt:
        # Register phone
        text = 'Welcome to Paysapp'
        res.message(text)
        ok = True

    if 'balance' in txt:
        # Default currency balance
        text = 'Your balance is 125.00 USD'
        res.message(text)
        ok = True

    if 'pay' in txt:
        text = 'Payment sent'
        res.message(text)
        ok = True

    if 'help' in action:
        text = 'Valid commands: hello, pay, balance'
        res.message(text)
        ok = True

    if not ok:
        text = "Invalid action. Type 'help' for more info"
        res.message(text)

    return str(res)



if __name__ == '__main__':
    app.run(debug=APP_DEBUG)

#END