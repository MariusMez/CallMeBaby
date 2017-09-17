import configargparse
from flask import Flask
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

app = Flask(__name__)

p = configargparse.ArgParser(default_config_files=['./config.txt'])
p.add('-c', '--config', required=False, is_config_file=True, help='config file path')
p.add('--account', required=True, help='Twilio account SID')  
p.add('--auth', required=True, help='Twilio authentication token')  
p.add('--number', required=True, help='Twilio Number start with +3')  
p.add('-to', required=True, help='Phone to call : eg. +33XXXXXXXXX')  

args = p.parse_args()
if not args.account:
    exit(parser.print_usage())

@app.route("/guigui/content", methods=['GET', 'POST'])
def content():
    response = VoiceResponse()
    response.say('Salut jeune Géocacheur !', voice='alice', language='fr-FR')
    response.play('http://demo.twilio.com/hellomonkey/monkey.mp3')

    return str(response)

@app.route("/guigui/call")
def call():

    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = args.account
    auth_token = args.auth
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=args.to,
        from_=args.number,
        url="http://www.mysolar.io/guigui/content",
        method='GET'
    )
    return call.sid

if __name__ == '__main__':
    app.run()
