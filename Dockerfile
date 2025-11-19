FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose port (optional)
EXPOSE 8000

# Use Azure injected port
ENV PORT=8000

# Start FastAPI using dynamic port
CMD ["sh", "-c", "uvicorn api_server:app --host 0.0.0.0 --port $PORT"]
