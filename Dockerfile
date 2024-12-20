# Dockerfile for python-app
FROM python:3.11.6

# Install git to clone repositories
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Keep container alive
CMD ["tail", "-f", "/dev/null"]