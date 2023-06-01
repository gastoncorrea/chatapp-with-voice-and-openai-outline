import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print('processing speech to text')
    audio_binary = request.data #Get the user's speech from their request
    text = speech_to_text(audio_binary) #call speech_to_text function to transcribe the speech 
   #Return the response back to user in JSON format 
    response = app.response_class(
       response = json.dumps({'text': text}),
       status = 200,
       mimeType = 'application/json')
    print(response)
    print(response.data)
    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    user_message = request.json['user_message']
    print('user Message: ', user_message)

    voice = request.json['voice']
    print('voice: ', voice)

    openai_response_text = openai_process_message(user_message)
    
    #clean the response to remove any emptylines
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

    # Call our text_to_speech function to convert OpenAI Api's reponse to speech
    openai_response_speech = text_to_speech(openai_response_text, voice)

    # convert openai_response_speech to base64 string so it can be sent back in the JSON response
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

    # Send a JSON response back to the user containing their message's response both in text and speech format
    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )

    # Send a JSON response back to the user containing their message's response both in text and speech formats
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
