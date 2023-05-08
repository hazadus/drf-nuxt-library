# Reference: https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
# Disables an automatic check for pip updates each time:
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# Python will not try to write .pyc files:
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures our console output is not buffered by Docker
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .