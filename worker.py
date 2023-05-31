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
    #Set up Watson text to speech HTTP API url
    base_url = 'https://sn-watson-tts.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    #Adding voice parameter in api url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    #Set the Headers for our HTTP request
    headers = {
        'Accept':'audio/wav',
        'Content-Type': 'application/json',
    }
    #Set the body of our HTTP request
    json_data ={
        'text': text
    }
    #Send a HTTP Post request to watson text to speech service
    response = requests.post(api_url,headers=headers,json=json_data)
    print('text to speech response:', response)
    return response.content


def openai_process_message(user_message):
    #Set the prompt for openai API
    prompt = "\"Actua como un asistente personal. Vos podes responder preguntas, traducir sentencias, agregar noticias, y dar recomendaciones."+user_message+"\""
    #Call the OpenAI API to process our prompt
    openai_response = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=4000)
    print("openai response: ", openai_response)
    #Parse the response to get the response text for our prompt
    response_text = openai_response.choices[0].text
    return response_text
