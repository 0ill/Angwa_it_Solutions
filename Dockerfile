FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for libsql and uvicorn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Create a script to run both Streamlit and FastAPI
# We'll use a simple shell script that runs both in background.
# For production, we can use a process manager like supervisord, but for simplicity we'll run them separately.

# Expose ports
EXPOSE 8501 8000

# Start both services
CMD ["sh", "-c", "uvicorn webhook_handler:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
