
import requests
import os

TOKEN_BOT = os.getenv('TOKEN_BOT')
PERSONA = os.getenv('CHAT_ID')


def SendToTelegram(msg, persona=PERSONA):
    try:
        url = 'https://api.telegram.org/bot{0}/sendMessage'.format(TOKEN_BOT)
        data = {
            'chat_id': persona,
            'text': msg
        }
        response = requests.post(url, data=data).json()
        return response
    except:
        #Fallisce perchè non hai settato bene il bot.
        pass
