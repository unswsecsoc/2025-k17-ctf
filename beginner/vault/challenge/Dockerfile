# Use official Python slim image
FROM python:3.13.7-slim-trixie

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask asgiref uvicorn

# Expose Flask port
EXPOSE 1337

# Run the Flask app
CMD ["uvicorn", "app:asgi_app", "--host", "0.0.0.0", "--port", "1337", "--workers", "8", "--reload"]
