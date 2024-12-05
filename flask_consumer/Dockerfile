# Dockerfile for python-app
FROM python:3.11.6

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Consume messages from Kafka
CMD ["python", "consume.py"]