FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["sh", "-c", "uvicorn api_server:app --host 0.0.0.0 --target-port ${PORT:-8000}"]




