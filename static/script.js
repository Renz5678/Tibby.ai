// Handle sending a message to the backend
function sendMessage() {
    const input = document.getElementById("query");
    const userMessage = input.value.trim();

    if (userMessage === "") return;

    // Show user's message
    addMessage("User", userMessage);

    // Disable input during response (optional UX feature)
    input.disabled = true;

    // Send message to Flask backend at /predict
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Show AI's response
        addMessage("Tibby", data.reply);
        input.value = "";
    })
    .catch(err => {
        console.error("Error:", err);
        addMessage("Tibby", "⚠️ Oops! Something went wrong.");
    })
    .finally(() => {
        input.disabled = false;
        input.focus();
    });
}

// Append a message to the chat content box
function addMessage(sender, message) {
    const chatContainer = document.querySelector(".chatcontent > div");
    const messageEl = document.createElement("div");

    messageEl.classList.add("messages__item");
    messageEl.classList.add(sender === "Tibby" ? "messages__item--visitor" : "messages__item--operator");
    messageEl.textContent = message;

    chatContainer.appendChild(messageEl);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Enable Enter key to send
document.addEventListener("DOMContentLoaded", () => {
    // Show greeting right away
    addMessage("Tibby", "👋 Hello, Gentinian! I am Tibby, GTDLNHS' cutest chatbot. How may I help you today?");

    // Enable Enter key to send
    const input = document.getElementById("query");
    input.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});

