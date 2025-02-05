#!/bin/bash
echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama server to be ready..."
while ! ollama list > /dev/null 2>&1; do  # Check if ollama list succeeds
    sleep 1
done
echo "Ollama server is ready."
echo "Attempting to pull ${MODEL_NAME}..."
ollama pull ${MODEL_NAME}
echo "Pull completed.  Starting ${MODEL_NAME}:"
sleep 10
ollama run ${MODEL_NAME}
echo "${MODEL_NAME} started."

tail -f /dev/null