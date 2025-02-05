# Chat with Your Local LLM (using Ollama and Flask)

This project sets up a chat interface using a local large language model (LLM) powered by Ollama, served through a Flask backend.

## Features

* Chat interface using HTML, and JavaScript.
* Flask backend to handle communication with the Ollama server.
* Dockerized setup for easy deployment and portability.
* GPU acceleration support for improved performance.


## Prerequisites

* **Docker:**  Install Docker Desktop or Docker Engine.
* **Docker Compose:** Install Docker Compose (included with Docker Desktop or install separately if needed).
* **NVIDIA Drivers and CUDA Toolkit (for GPU usage):** If you want to use GPU acceleration, you'll need:
    - NVIDIA drivers compatible with your GPU.
    - CUDA Toolkit and cuDNN. Make sure these versions are compatible with your NVIDIA drivers and any deep learning frameworks used by Ollama (e.g. PyTorch or TensorFlow).
    - `nvidia-container-toolkit`:  Follow the NVIDIA documentation for installation instructions.

## Installation

1. **Clone the Repository:**
    ```
    git clone https://github.com/SomniferousWallaby/LLMInABox
    cd LLMInABox
    ``` 

2. **Update the .env file:** 
Update the .env file in the project's root directory and set the following environment variables:
    ```
    MODEL_NAME=deepseek-r1:32b # Or the name of the model you want to use in Ollama. This should be automatically pulled into your ollama container when run through docker-compose.
    OLLAMA_API_URL=http://ollama:11434/api/generate
    ```
3. **Build the Docker Images:**

    ```docker compose build --no-cache```

4. **Run the Docker Containers:**

    ```docker compose up -d```

## Usage
Open your web browser and go to http://localhost:5000 to access the chat interface. Type your messages and click "Send" or press Enter.

*Note: The container may take a while to initially start, depending on the size of the model you select. The model is downloaded inside the ollama docker container on launch, and needs to finish downloading before the app will function properly.* 

## GPU Acceleration
To enable GPU acceleration, make sure you have the NVIDIA drivers, CUDA Toolkit, and nvidia-container-toolkit installed on your host machine (see Prerequisites). The docker-compose.yml file is NOT configured to use the NVIDIA runtime or make the GPU available to the Ollama container by default.

The `NVIDIA_VISIBLE_DEVICES=all` setting in the `docker-compose.yml` file makes all GPUs on your host visible to the Ollama container. If you have multiple GPUs and only want to use a specific one, change all to the GPU ID (e.g., 0 for the first GPU, 1 for the second, etc.).

After starting the docker containers, running the command ollama list within the Ollama container should indicate GPU availability and memory usage. If the model requires more vram than your GPU has, it will not run on your GPU. Please be sure to check your specific model for requirements.

## Troubleshooting
- **Ollama server not running:** Check the logs of the ollama container (docker logs <container-name>) for any error messages. Ensure the model specified by MODEL_NAME is available to Ollama.
- **Flask app errors:** Check the logs of the chat-app container for errors related to network communication or response handling.
"Unexpected token '<'" error: This indicates that the Flask app is returning HTML instead of JSON. Double-check all return paths in the /chat route to ensure they use jsonify().
- **GPU not being used:** Ensure the necessary NVIDIA drivers, CUDA Toolkit, and nvidia-container-toolkit are installed on your host machine. Verify that Ollama can see the GPU by running nvidia-smi inside the container. Check the ollama container logs for any GPU-related errors.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.