from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather


app = Flask(__name__)

@app.route('/gilbert_ivr',methods=['GET','POST'])
def gilbert_ivr(request):
    response = VoiceResponse()

    gather = Gather(num_digits=1,action='/gather')
    gather.say('Press 7 to prove your not a bot')
    response.append(gather)

    response.redirect('/gilbert_ivr')

@app.route('/gather',methods=['GET','POST'])
def gather():
    response = VoiceResponse()
    if 'Digits' in request.values:
        selected_option = request.form['Digits']
        choice = request.values['Digits']
        option_actions = {'7':'+15879882049'}
        if choice == '7':
            response.dial(option_actions[selected_option])
            return twiml(response)

