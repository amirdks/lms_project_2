
var userName = "{{ username }}";
alert(userName)
var socket = new WebSocket(
    'ws://' + window.location.host +
    '/ws/chat/' + userName + '/');
