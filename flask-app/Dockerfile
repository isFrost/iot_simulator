# Dockerfile for python-app
FROM python:3.11.6

# Set the working directory
WORKDIR /flask-app

# Copy app files
COPY . .

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5555

# Start Flask app
CMD ["python", "flask_app.py"]