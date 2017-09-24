import configargparse
import cherrypy
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say
from cherrypy.process.plugins import Daemonizer
d = Daemonizer(cherrypy.engine)
d.subscribe()

p = configargparse.ArgParser(default_config_files=['./config.txt'])
p.add('-c', '--config', required=False, is_config_file=True, help='config file path')
p.add('--account', required=True, help='Twilio account SID')  
p.add('--auth', required=True, help='Twilio authentication token')  
p.add('--number', required=True, help='Twilio Number start with +3')  
p.add('-to', required=False, help='Phone to call : eg. +33XXXXXXXXX')  

args = p.parse_args()
if not args.account:
    exit(parser.print_usage())

class CallMeBaby(object):
    @cherrypy.expose
    def content(self, url, **params):
        response = VoiceResponse()
        #response.say('Salut jeune Géocacheur !', voice='alice', language='fr-FR')
        #response.play('http://veroguigui83.free.fr/ValEvent/message-la-source.mp3')
        print(str(url))
        response.play(str(url))
        return str(response)

    @cherrypy.expose
    def call(self, num, url, **params):
        # Your Account Sid and Auth Token from twilio.com/user/account
        account_sid = args.account
        auth_token = args.auth
        number = args.number
        url_xml = "http://www.mysolar.io/callmebaby/content?url="+str(url)
        print(url_xml)
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=num,
            from_=number,
            url=url_xml,
            method='GET'
        )
        return call.sid

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 5000,
        'tools.proxy.on': True,
        'tools.proxy.base': 'http://www.mysolar.io'
    })
    cherrypy.quickstart(CallMeBaby(),'/callmebaby')
