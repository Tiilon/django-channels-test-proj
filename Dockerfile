# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update -y && apt-get install -y \
    pkg-config \
    python3-dev \
    build-essential \
    default-libmysqlclient-dev \
    --no-install-recommends

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY . .

# Collect static files (if using)
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
