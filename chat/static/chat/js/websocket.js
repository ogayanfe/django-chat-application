// Global => ScrollToBottom, getMessagHtmlText, host

const wsprotocol = host === "https" ? "wss" : "ws";
const groupId = document.getElementById("group_id").value;
const websocketurl = `${wsprotocol}://${host}/ws/chat/${groupId}/`;
const userId = document.querySelector("#id-user-id").value;
const retryFrequency = 1600; // Unit -> milliseconds
let CONNECTED_TO_SERVER = false;
let socket;

function addAttributesToSocket(socket) {
    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        appendMessage(data, (owner = data.owner == userId));
    };

    socket.onerror = (e) => {
        console.log(console.error(e));
    };

    socket.onclose = () => {
        console.log("Disconnected");
        CONNECTED_TO_SERVER = false;
        connectToServer();
    };
}

function makeConnection(action) {
    // It takes a callback function
    let chatSocket = new WebSocket(websocketurl);
    const connect = setInterval(() => {
        // Using setInterval is neccessary because i want to keep
        // tring to connect to the server until the socket is open

        console.log("Connecting");
        if (chatSocket.readyState === WebSocket.OPEN) {
            // The server is connected
            clearInterval(connect); // Clear the interval
            action(chatSocket); // call the callback with takes the newly created socket
            console.log("Connected");
        } else if (chatSocket.readyState === WebSocket.CLOSED) {
            console.error(`Socket closed, retrying in ${retryFrequency / 1000}s`); // Connection failed
            chatSocket = new WebSocket(websocketurl); // Try to connect again
        }
    }, 2000);
}

function connectToServer() {
    makeConnection((newSocket) => {
        addAttributesToSocket(newSocket);
        socket = newSocket;
        CONNECTED_TO_SERVER = true;
    });
}

function appendMessage(message, owner) {
    const { content, username, created_date, profile_picture, active_count } = message;
    const messageArea = document.querySelector(".messages");
    const messageHtmlText = getMessageHtmlText(
        content,
        username,
        owner,
        profile_picture,
        created_date
    );
    messageArea.innerHTML += messageHtmlText;
    document.getElementById("active-members-count").textContent = active_count - 1;
    scrollToBottom();
}

document.querySelector(".message-input-container").addEventListener("submit", (e) => {
    e.preventDefault();
    if (!CONNECTED_TO_SERVER) {
        alert("Error sending message, check you network connection");
        return;
    }
    const messageInputEl = e.target.message;
    const message = messageInputEl.value;
    if (message.length < 1) return;
    socket.send(JSON.stringify({ message: message }));
    messageInputEl.value = "";
});

connectToServer();
