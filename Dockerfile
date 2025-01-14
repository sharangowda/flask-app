# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the instance directory
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Copy the application files
COPY . .

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=1

# Run the application
CMD ["python", "main.py"] 