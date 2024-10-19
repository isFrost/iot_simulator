# Dockerfile for python-app
FROM python:3.12.3

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

# Clone the project from GitHub (if necessary, replace with actual repo URL)
# RUN git clone https://github.com/yourusername/yourproject.git .

# Default command (override in docker-compose if needed)
CMD ["python", "main.py"]