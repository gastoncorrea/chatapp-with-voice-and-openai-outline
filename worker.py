import openai
import requests

openai.api_key = "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"


def speech_to_text(audio_binary):
    #Set up Watson Speech to Text HTTP Api url
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    #Set up parameters for our HTTP request
    params = {
        'model':'es-LA_Multimedia',
    }
    #Set up the body of our HTTP request
    body = audio_binary

    #Send a HTTP Post request
    response = requests.post(api_url, params=params, data=body).json()

    #parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response', response)
        text = response.get('results').pop().get('alternative').pop().get('transcript')
        print('recognised text: ', text)
    return text


def text_to_speech(text, voice=""):
    return None


def openai_process_message(user_message):
    return None
