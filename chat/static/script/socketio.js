document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const messageContainer = document.getElementById('message-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const privateChatButtons = document.getElementsByClassName('private-chat-btn');

    let otherUserId = null; // Store the other user ID

    // Join private chat room with the specified user
    function joinPrivateChat(userId, username) {
        otherUserId = userId; // Set the other user ID
        otherUserUsername = username; // Set the other user username
        socket.emit('join_private_chat', { other_user_id: userId });
        document.getElementById('send-button').style.display = 'block'; // Show send button
        document.getElementById('message-input').style.display = 'block';
        messageContainer.innerHTML = ''; // Clear previous messages
        socket.emit('get_previous_private_messages', { room: `${userId}_${currentUserId}` });
    }




    

        // Handle incoming private messages
        socket.on('new_private_message', (data) => {
            const messageElement = document.createElement('div');
            messageElement.innerText = `Sender: ${data.sender_id}--- ${data.content}`;
            messageContainer.appendChild(messageElement);
            messageElement.style.border = '1px solid black';
            messageElement.style.color = 'cyan'; // Set the style for the message
            messageElement.style.padding = '10px'; 
            messageElement.style.marginBottom = '10px';
            messageElement.style.backgroundColor = 'green';
            messageElement.style.minWidth = '200px'; // Set a minimum width for the message box
            messageElement.style.width = 'fit-content'; // Allow the message box to expand based on content
            messageInput.value = '';    
            messageContainer.insertBefore(messageElement, messageContainer.firstChild);        
        });

      

    // Display previous private messages
    socket.on('previous_private_messages', (data) => {
        const messages = data.messages.reverse(); // Reverse the order of messages
        for (let i = 0; i < messages.length; i++) {
            const messageElement = createMessageElement(messages[i]);
            messageContainer.appendChild(messageElement);
        }
    });

    // Send private message
    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const message = messageInput.value;

        socket.emit('send_private_message', { other_user_id: otherUserId, content: message });

        const messageElement = createMessageElement({
            sender_id: currentUserId,
            content: message
        });
        messageContainer.insertBefore(messageElement, messageContainer.firstChild);

        messageInput.value = '';
    });

    // Helper function to create a message element
    function createMessageElement(message) {
        const messageElement = document.createElement('div');
        messageElement.innerText = `Sender: ${message.sender_id} --- ${message.content}`;
        messageElement.style.border = '1px solid black';
        messageElement.style.color = 'green';
        messageElement.style.padding = '10px';
        messageElement.style.marginBottom = '10px';
        messageElement.style.backgroundColor = 'black';
        messageElement.style.minWidth = '200px';
        messageElement.style.width = 'fit-content';
        return messageElement;
    }

    // Attach event listeners to private chat buttons
    for (let i = 0; i < privateChatButtons.length; i++) {
        const button = privateChatButtons[i];
        const userId = button.getAttribute('data-user-id');
        button.addEventListener('click', () => {
            // Update the UI or perform any desired action
            removeClickedClassFromButtons(); // Remove the 'clicked' class from all buttons
            button.classList.add('clicked'); // Add the 'clicked' class to the clicked button
            joinPrivateChat(userId);
        });
    }

    // Helper function to remove the 'clicked' class from all buttons
    function removeClickedClassFromButtons() {
        for (let i = 0; i < privateChatButtons.length; i++) {
            privateChatButtons[i].classList.remove('clicked');
        }
    }

});


