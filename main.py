from flask import escape
import utils
from twilio.twiml.voice_response import VoiceResponse, Play

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def gilbert_ivr(request):
    selected_option = request.form.get('Digits')
    michaels_number = '+15879882049'
    known_traitors = ['+15879999999']
    contact = request.form.get('From')
    calling = request.form.get('To')
    base_url = 'https://storage.googleapis.com/gilbert_ivr/'
    thank_you = f'{base_url}thank_you.mp3'
    goodbye = f'{base_url}goodbye.mp3'
    press_7 = f'{base_url}press_7.mp3'

    # Handle user input
    if calling == '+15876022966':
        contact_list = f'{config.PROJECT_ID}.{config.DATASET_ID}.{config.TABLE_ID}'
        logger.info(contact_list)
        personal_contacts = utils.get_contacts(contact_list=contact_list)
        if selected_option is None:
            response = VoiceResponse()
            # response.say('To speak to Michael, press 7.')
            response.play(press_7)
            gather = response.gather(num_digits=1,actions='/gilbert_ivr',method='POST')

        elif selected_option == '7':
            response = VoiceResponse()
            # response.say('Thank you. I will forward your call now.')
            response.dial(michaels_number)
            response.play(thank_you)


        else:
            # If no valid option is selected, end the call
            response = VoiceResponse()
            response.play(f'{base_url}goodbye.mp3')
            # response.say('Thanks for calling. Goodbye.')

    elif calling == '+15878176449':
        realist_contacts = []

        if contact in realist_contacts:
            response = VoiceResponse()
            response.dial(michaels_number)

        elif selected_option is None:
            response = VoiceResponse()
            response.say('Thanks for calling Realist Consulting! To speak to Michael Gilbert press 7')
            # response.play(f'{base_url}press_7.mp3')
            gather = response.gather(num_digits=1, actions='/realist_ivr', method='POST')

        elif selected_option == '7':
            response = VoiceResponse()
            response.say('Thank you, I will forward you now.')
            # response.play(f'{base_url}thank_you.mp3')
            response.dial(michaels_number)

        else:
            response = VoiceResponse()
            # response.play(f'{base_url}thank_you.mp3')
            response.say('Goodbye, and have a great day!')

    return str(response)
