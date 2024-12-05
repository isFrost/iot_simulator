// Function to fetch latest messages and update the list
async function fetchMessages() {
    try {
        const response = await fetch('/latest_messages');
        const data = await response.json();

        // Get the main container for room divs
        const messagesContainer = document.getElementById('messages-container');

        // Clear the existing room data
        messagesContainer.innerHTML = '';

        // Organize messages by room and parameter
        const roomMessages = {};
        const roomSummaries = {};

        // Group messages by room and limit to the latest 200 messages
        data.messages.forEach(message => {
            const roomId = message.room;  // Assumes message contains a "room" field
            const parameter = message.parameter;

            // Initialize data structure for each room
            if (!roomMessages[roomId]) {
                roomMessages[roomId] = [];
                roomSummaries[roomId] = {};
            }

            // Keep only the latest 200 messages per room
            roomMessages[roomId].push(message);
            if (roomMessages[roomId].length > 200) {
                roomMessages[roomId].shift();
            }

            // Update the latest readings by parameter for the room summary
            if (!roomSummaries[roomId][parameter]) {
                roomSummaries[roomId][parameter] = [];
            }
            roomSummaries[roomId][parameter] = message;  // Update latest message for the parameter
        });

        // Populate each room's div with its messages and latest summary
        for (const roomId in roomMessages) {
            // Create a div for the room if it doesn't exist
            const roomDiv = document.createElement('div');
            roomDiv.classList.add('room');
            roomDiv.id = `room-${roomId}`;

            // Room header
            const roomHeader = document.createElement('h2');
            roomHeader.textContent = `Room ${roomId}`;
            roomDiv.appendChild(roomHeader);

            // Summary of latest measurements
            const summaryDiv = document.createElement('div');
            summaryDiv.classList.add('summary');
            for (const [parameter, latestMessage] of Object.entries(roomSummaries[roomId])) {
                const summaryText = document.createElement('p');
                summaryText.textContent = `${parameter}: sensor #${latestMessage.sensor}: ${latestMessage.value} ${latestMessage.unit}`;
                summaryDiv.appendChild(summaryText);
            }
            roomDiv.appendChild(summaryDiv);

            // List of messages for this room
            const messagesList = document.createElement('ul');
            roomMessages[roomId].forEach(message => {
                const listItem = document.createElement('li');

                // Format the message data
                const formattedMessage = `Timestamp: ${message.timestamp}, Parameter: ${message.parameter}, Room: ${message.room}, Sensor: ${message.sensor}, Status: ${message.status}, Value: ${message.value}, Unit: ${message.unit}`;
                listItem.textContent = formattedMessage;

                messagesList.appendChild(listItem);
            });

            // Append the scrollable list to the room div
            roomDiv.appendChild(messagesList);
            messagesContainer.appendChild(roomDiv);
        }
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

// Refresh messages every 5 seconds
setInterval(fetchMessages, 5000);

// Initial fetch when the page loads
window.onload = fetchMessages;