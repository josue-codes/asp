# For Python 3.11
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Ensuring necessary components are installed for library compilation
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    python3-dev

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the code to the working directory
#COPY . .