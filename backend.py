from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

app = Flask(__name__)

#DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_API_URL = "http://localhost:11434/api/generate"
conversation_history = {}

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

    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "model": "deepseek-r1:32b",
        "prompt": "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]),
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9,
        "stream": True
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, stream=True)
        response.raise_for_status()
        full_response = ""
    
        for chunk in response.iter_lines(decode_unicode=True):
            if chunk:
                try:
                    chunk_json = json.loads(chunk)
                    full_response += chunk_json.get("response")

                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON chunk: {e}")

        history.append({"role": "assistant", "content": full_response}) # Store Deepseek's response
        conversation_history[session_id] = history # Update the history for this session
        return jsonify({'response': full_response, 'session_id': session_id})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)