from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

# store received messages
messages = []


# Route to receive HTTP POST requests
@app.route('/receive', methods=['POST'])
def receive_message():
    message = request.get_json()
    print(f"Received message: {message}")
    messages.append(message)  # Store the message in the global list
    return jsonify({"status": "success", "message": message}), 200


# Endpoint to get the latest messages as JSON
@app.route('/latest_messages', methods=['GET'])
def latest_messages():
    return jsonify(messages=messages)


# Route to display the received messages
@app.route('/messages', methods=['GET'])
def display_messages():
    return render_template('messages.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
