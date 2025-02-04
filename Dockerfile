# Use a suitable base image (Python 3.9 Slim in this example)
FROM python:3.9-slim-buster

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY backend.py .
COPY templates/chat.html .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Start the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend:app"]