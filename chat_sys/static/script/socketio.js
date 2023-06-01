// socketio.js
$(document).ready(function() {
  var socket = io.connect('http://127.0.0.1:5000');

  // Emit join event to join the chat room
  socket.emit('join', { room: 'chat' });

  // Handle connected event
  socket.on('connected', function(data) {
    console.log('Connected to server');
  });

  // Handle join_room event
  socket.on('join_room', function(data) {
    console.log('Joined chat room');
  });

  // Handle leave_room event
  socket.on('leave_room', function(data) {
    console.log('Left chat room');
  });

  // Handle message event
  socket.on('message', function(data) {
    var sender = data.sender;
    var message = data.message;
    $('#chat-messages').append('<p><strong>' + sender + ':</strong> ' + message + '</p>');
  });

  // Handle form submission
  $('#chat-form').submit(function(e) {
    e.preventDefault();
    var receiver = $('#receiver-select').val();
    var message = $('#message-input').val();

    // Emit message event
    socket.emit('message', {
      sender: 'User1', // Replace with actual sender name or ID
      receiver: receiver,
      message: message
    });

    $('#message-input').val('');
  });
});
