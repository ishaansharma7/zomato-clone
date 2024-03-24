# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev gcc \
    && pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Django project files to the working directory
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Run Gunicorn
# CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
