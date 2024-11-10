FROM python:3.11.6

WORKDIR /flask-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5555

CMD ["python", "flask_app.py"]