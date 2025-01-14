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

# Copy the .env file first
COPY .env .env

# Copy the rest of the application
COPY . .

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Use gunicorn config file
COPY gunicorn.conf.py .

# Run the application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"] 