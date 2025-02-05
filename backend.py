from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import json
import uuid
import os

MODEL_NAME=os.environ.get("MODEL_NAME")
if not MODEL_NAME:
    raise RuntimeError("MODEL_NAME environment variable not set.")

load_dotenv()

app = Flask(__name__)

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL")
app.logger.info('%s Ollama API URL set as:', OLLAMA_API_URL)
if not OLLAMA_API_URL:
    raise RuntimeError("OLLAMA_API_URL environment variable not set.")

conversation_history = {}

@app.route('/test_json')
def test_json():
    return jsonify({"message": "This is a JSON response"})

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    session_id = request.json.get('session_id')
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    history = conversation_history.get(session_id, [])
    history.append({'role': 'user', 'content': user_message})
    app.logger.info('%s User message added to history:', session_id, ': ', user_message)

    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "model": MODEL_NAME,
        "prompt": "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]),
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9,
        "stream": True
    }
    
    try:
        app.logger.debug(f"Received user message: {user_message}")
        app.logger.debug(f"Session ID: {session_id}")
        app.logger.debug(f"Sending request to {OLLAMA_API_URL}: {data}")

        response = requests.post(OLLAMA_API_URL, headers=headers, json=data, stream=True)
        app.logger.debug(f"Received response from Ollama, status code: {response.status_code}")
        response = requests.post(OLLAMA_API_URL, headers=headers, json=data, stream=True)
        response.raise_for_status()
        full_response = ""
    
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                try:
                    chunk_json = json.loads(chunk)
                    full_response += chunk_json.get("response")

                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON chunk: {e}")

        history.append({"role": "assistant", "content": full_response}) # Store Ollama's response
        conversation_history[session_id] = history # Update the history for this session
        app.logger.info('%s Response message added to history:', session_id, ': ', full_response)
        return jsonify({'response': full_response, 'session_id': session_id})

    except Exception as e:
        app.logger.error(f"Error in /chat route: {e}")
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)