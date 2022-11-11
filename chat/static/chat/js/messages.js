// Global --> host, httpprotocol, scrollToBottom
const roomId = parseInt(document.getElementById("group_id").value);
const roomMessagesApiUrl = httpprotocol + "//" + host + "/chat/api/room/" + roomId + "/";

const getMessages = async () => {
    try {
        const response = await fetch(roomMessagesApiUrl);
        const data = await response.json();
        if (response.status === 200) return data;
    } catch (error) {
        console.log(error);
        return [];
    }
};

function updateMessagesHeader(topic, number_of_members, active_members, dp) {
    const messageSection = document.querySelector(".message-section-header");
    messageSection.innerHTML = `
    <div class="conversation-info">
    <img
    src="${dp}"
    alt="group dp"
    srcset=""
    class="profile-image"
    />
    <div>
    <h3 class="group-name">${topic}</h3>
    <div>${number_of_members} Members, You and <span id="active-members-count">${active_members}</span> active members</div>
    </div>
    </div>
    `;
}

function getMessageHtmlText(content, owner_username, isOwner, user_profile_picture, created_date) {
    return `<div class="msg ${isOwner && "owner"}">
    <div>
    <img
        src="${user_profile_picture}"
    alt="${owner_username} profile picture"
    class="profile-image"
    />
    </div>
    <div class="msg-body">
    <h4 style="color:rgb(123, 187, 239); text-transform: capitalize;">${owner_username}</h4>
    <div>${content}</div>
    <span>${created_date}</span>
    </div>
    </div>`;
}

function updateMembersList(members) {
    const membersHtmlText = members
        .map(({ username, profile_image, active }) => {
            return `
            <div class="user-group">
                <img src="${profile_image}" class="profile-image"/>
                <p style="margin-right: auto">@${username}</p>
                ${
                    active
                        ? "<p style='color: white; font-size: 12px; padding-right: 10px'>active now</p>"
                        : ""
                }
            </div>   
        `;
        })
        .join("");
    const node = document.querySelector(".user-list");
    if (node) node.innerHTML = membersHtmlText;
}

(async function displayMessages() {
    const data = await getMessages();
    const { topic, number_of_members, active_members_count, dp, members } = data;
    const messagesHtmlElementStr = document.querySelector(".messages");
    updateMessagesHeader(topic, number_of_members, active_members_count, dp);
    updateMembersList(members);
    const messageHtmlEl = data.messages.map((item) => {
        return getMessageHtmlText(
            item.content,
            item.owner_username,
            item.is_owner,
            item.user_profile_picture,
            item.time_created_string
        );
    });
    messagesHtmlElementStr.innerHTML += messageHtmlEl.join("");
    scrollToBottom();
})();
