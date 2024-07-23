FROM --platform=linux/amd64 python:3.12-slim as build

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:$PATH"

# Variables references to be used in the build, from the DevOps pipeline
ARG tenant_id
ARG client_id
ARG client_secret
ARG sendgrid_api_key
ARG subject

# Environment variables
ENV tenant_id=${tenant_id}
ENV client_id=${client_id}
ENV client_secret=${client_secret}
ENV SENDGRID_API_KEY=${sendgrid_api_key}
ENV subject=${subject}

# Set label
LABEL description="Python solution to query and send by email a secrets expiration report"
LABEL author="ErikRodriguezVitier"

# Install system dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the source code to the container
COPY . /app

# Run the application
CMD ["python", "app.py"]