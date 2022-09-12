const host = window.location.host;
const httpprotocol = window.location.protocol;
const roomListApiView = httpprotocol + "//" + host + "/chat/api/all_rooms/?search=";
const chat_room_name = document.getElementById("id-room_name").value;

function viewConversation(event) {
    const node = event;
    const path = node.getAttribute("data--href");
    if (window.location.pathname !== path) window.location = path;
}

function conversationListHtml(data) {
    const { topic, last_message, last_updated, get_absolute_url, dp } = data;
    const message_last_sent = last_message
        ? last_message.length > 45
            ? last_message.slice(0, 45) + "..."
            : last_message
        : "";
    return `
    <div class="conversation ${
        topic === chat_room_name && "active"
    }" role="link" data--href="${get_absolute_url}" onclick="viewConversation(this)">
        <div class="conversation-info">
            <img
                src="${dp}"
                alt="${topic} profile"
                class="profile-image"
            />
            <div>
                <h3 class="group-name">${topic}</h3>
                <div>${message_last_sent}</div>
            </div>
        </div>
        <span class="conversation-last-time">${last_updated ? last_updated : ""}</span>    
    </div>
    `;
}

// function messageListHtml(data) {}

const getChatRooms = async () => {
    try {
        const response = await fetch(roomListApiView);
        if (response.status !== 200) return [];
        const data = await response.json();
        return data;
    } catch (error) {
        return [];
    }
};

(async () => {
    const data = await getChatRooms();
    const parent = document.querySelector(".conversation-lists");
    const chatListElements = data.map((item) => conversationListHtml(item));
    parent.innerHTML = chatListElements.join("");
    const activeNode = document.querySelector(".conversation.active");
    if (activeNode) activeNode.scrollIntoView({ behavior: "smooth" });
})();

function scrollToBottom() {
    const node = document.querySelector(".msg:last-child");
    if (node) node.scrollIntoView({ behavior: "smooth" });
}
