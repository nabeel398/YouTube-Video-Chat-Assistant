FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with timeout and retry
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --timeout 100 -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p instance/faiss_index logs

EXPOSE 8000

# Run with reload for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]