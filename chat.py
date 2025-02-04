import requests
import json

def chat_with_deepseek(prompt):
    """Sends a prompt to Deepseek and handles streaming responses."""
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "deepseek-r1:32b", "prompt": prompt}

    with requests.post(url, headers=headers, json=data, stream=True) as response:
        response.raise_for_status()
        full_response = ""
        for chunk in response.iter_lines(decode_unicode=True):  # Decode as Unicode
            try:
                chunk_json = json.loads(chunk)
                full_response += chunk_json["response"]
                if chunk_json.get("done", False):
                    break  # Stop when done
            except json.JSONDecodeError as e:
                print(f"Warning: Ignoring invalid JSON chunk: {e}") # Handle potential errors gracefully

    return full_response

if __name__ == "__main__":
    while True:
        prompt = input("You: ")
        response = chat_with_deepseek(prompt)
        print(f"Deepseek: {response}")