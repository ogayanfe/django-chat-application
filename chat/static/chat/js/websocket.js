const wsprotocol = host === "https" ? "wss" : "ws";
const groupId = document.getElementById("group_id").value;
const websocketurl = `${wsprotocol}://${host}/ws/chat/${groupId}/`;
const userId = document.querySelector("#id-user-id").value;

let CONNECTED_TO_SERVER = false;

document.querySelector(".message-input-container").addEventListener("submit", (e) => {
    e.preventDefault();
    const messageInputEl = e.target.message;
    const message = messageInputEl.value;
    if (message.length < 1) return;
    chatSocket.send(JSON.stringify({ message: message }));
    messageInputEl.value = "";
});

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

const chatSocket = new WebSocket(websocketurl);

chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    appendMessage(data, (owner = data.owner == userId));
};

chatSocket.onopen = (e) => {
    CONNECTED_TO_SERVER = true;
};

chatSocket.onerror = (e) => {
    console.log(console.error());
};

chatSocket.onclose = () => {
    console.log("Disconnected");
    CONNECTED_TO_SERVER = false;
};
