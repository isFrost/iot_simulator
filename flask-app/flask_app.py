from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

messages = []    # store received messages


@app.route('/receive', methods=['POST'])
def receive_message():
    """
    Route to receive HTTP POST requests
    """
    message = request.get_json()
    messages.append(message)  # Store the message in the global list
    return jsonify({"status": "success", "message": message}), 200


@app.route('/latest_messages', methods=['GET'])
def latest_messages():
    """
    Endpoint to get the latest messages as JSON
    """
    return jsonify(messages=messages)


@app.route('/messages', methods=['GET'])
def display_messages():
    """
    Route to display the received messages
    """
    return render_template('messages.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
