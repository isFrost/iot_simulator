# Dockerfile for python-app
FROM python:3.11.6

# Set the working directory
WORKDIR ./db-consumer

# RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python3 pip

# Copy app files
COPY . .

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start consuming messages
CMD ["python3", "consume.py"]