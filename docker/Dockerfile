# Use the latest Alpine Linux
FROM alpine:latest

# Set the working directory in the Docker image
WORKDIR /root/main/

# Copy everything in the current directory to the working directory in the Docker image
COPY server.py client.py .env ./

# Install python3, pip and venv
RUN apk add --no-cache python3 py3-pip python3-dev build-base linux-headers \
    && python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip

# Install dependencies using the virtual environment
RUN /venv/bin/pip install python-dotenv

