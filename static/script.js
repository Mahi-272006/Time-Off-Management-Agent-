const sendBtn = document.getElementById("sendBtn");
const messageInput = document.getElementById("messageInput");
const chatBox = document.getElementById("chatMessages");
const employeeInput = document.getElementById("employeeId");

function addMessage(sender, text) {

    const wrapper = document.createElement("div");

    wrapper.className = `message ${sender}`;

    if(sender === "bot"){

        wrapper.innerHTML = `
            <div class="avatar bot-avatar">🤖</div>

            <div class="bubble">

                <p>${text}</p>

                <span class="msg-time">
                    ${new Date().toLocaleTimeString([], {
                        hour: '2-digit',
                        minute:'2-digit'
                    })}
                </span>

            </div>
        `;

    }else{

        wrapper.innerHTML = `
            <div class="bubble">

                <p>${text}</p>

                <span class="msg-time">
                    ${new Date().toLocaleTimeString([], {
                        hour:'2-digit',
                        minute:'2-digit'
                    })}
                </span>

            </div>
        `;

    }

    chatBox.appendChild(wrapper);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    const employeeId = employeeInput.value;

    if (!message) return;

    if (!employeeId) {
        alert("Please enter Employee ID");
        return;
    }

    addMessage("user", message);

    messageInput.value = "";

    try {
        addMessage("bot", "Thinking...");
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                employee_id: employeeId,
                message: message
            })
        });

        const data = await response.json();

        chatBox.removeChild(chatBox.lastElementChild);

        addMessage("bot", data.response);

    } catch (err) {
        console.error(err);
        addMessage("bot", "Something went wrong.");
    }
}

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});