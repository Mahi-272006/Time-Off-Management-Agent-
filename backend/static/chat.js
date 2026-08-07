const messages = document.getElementById("messages");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");

function addMessage(role, text) {

    const row = document.createElement("div");
    row.className =
        role === "user"
            ? "message-row user-row"
            : "message-row assistant-row";

    const avatar = document.createElement("div");
    avatar.className =
        role === "user"
            ? "avatar user-avatar"
            : "avatar assistant-avatar";

    avatar.innerHTML =
        role === "user"
            ? "👤"
            : "🤖";

    const bubble = document.createElement("div");
    bubble.className =
        role === "user"
            ? "message user-message"
            : "message assistant-message";

    bubble.innerHTML = text.replace(/\n/g, "<br>");

    if (role === "assistant") {
        row.appendChild(avatar);
        row.appendChild(bubble);
    } else {
        row.appendChild(bubble);
        row.appendChild(avatar);
    }

    messages.appendChild(row);

    messages.scrollTop = messages.scrollHeight;
}

function showTyping() {

    const row = document.createElement("div");

    row.className = "message-row assistant-row";

    row.id = "typing";

    row.innerHTML = `

        <div class="avatar assistant-avatar">
            🤖
        </div>

        <div class="message assistant-message">

            Thinking...

        </div>

    `;

    messages.appendChild(row);

    messages.scrollTop = messages.scrollHeight;
}

function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) {
        typing.remove();
    }
}

async function sendMessage() {

    const text = input.value.trim();

    if (text === "") return;

    addMessage("user", text);

    input.value = "";

    showTyping();

    sendBtn.disabled = true;

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        removeTyping();

        addMessage("assistant", data.response);

    }

    catch (err) {

        removeTyping();

        addMessage(
            "assistant",
            "❌ Unable to connect to backend."
        );

        console.error(err);

    }

    sendBtn.disabled = false;

}

input.addEventListener("keydown", function (e) {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        sendMessage();

    }

});

async function logout() {

    await fetch("/logout");

    window.location = "/";

}