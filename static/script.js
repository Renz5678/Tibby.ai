// ---------------------------
// Chatbot Functions
// ---------------------------

// Handle sending a message to the backend
function sendMessage() {
    const input = document.getElementById("query");
    const userMessage = input.value.trim();

    if (userMessage === "") return;

    // Show user's message with animation
    addMessage("User", userMessage);

    // Clear input and disable during response
    input.value = "";
    input.disabled = true;

    // Show typing indicator
    showTypingIndicator();

    // Send message to Flask backend at /chat
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Remove typing indicator
        removeTypingIndicator();
        
        // Show AI's response with typing effect
        addMessageWithTyping("Tibby", data.reply);
    })
    .catch(err => {
        console.error("Error:", err);
        removeTypingIndicator();
        addMessage("Tibby", "⚠️ Oops! Something went wrong.");
    })
    .finally(() => {
        input.disabled = false;
        input.focus();
    });
}

// Append a message to the chat with fade-in animation
function addMessage(sender, message) {
    const chatContainer = document.querySelector(".chatcontent > div");
    const messageEl = document.createElement("div");

    messageEl.classList.add("messages__item");
    messageEl.classList.add(sender === "Tibby" ? "messages__item--visitor" : "messages__item--operator");
    messageEl.style.opacity = "0";
    messageEl.style.transform = "translateY(10px)";
    messageEl.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    
    // Handle line breaks and formatting
    messageEl.innerHTML = formatMessage(message);

    chatContainer.appendChild(messageEl);

    // Trigger animation
    setTimeout(() => {
        messageEl.style.opacity = "1";
        messageEl.style.transform = "translateY(0)";
    }, 10);

    scrollToBottom();
}

// Add message with typing effect for bot responses
function addMessageWithTyping(sender, message) {
    const chatContainer = document.querySelector(".chatcontent > div");
    const messageEl = document.createElement("div");

    messageEl.classList.add("messages__item");
    messageEl.classList.add("messages__item--visitor");
    messageEl.style.opacity = "0";
    messageEl.style.transform = "translateY(10px)";
    messageEl.style.transition = "opacity 0.3s ease, transform 0.3s ease";

    chatContainer.appendChild(messageEl);

    // Fade in the message bubble
    setTimeout(() => {
        messageEl.style.opacity = "1";
        messageEl.style.transform = "translateY(0)";
    }, 10);

    // Start typing effect after fade-in
    setTimeout(() => {
        typeMessage(messageEl, message);
    }, 300);

    scrollToBottom();
}

// Typing effect function
function typeMessage(element, message, speed = 20) {
    let index = 0;
    const formattedMessage = formatMessage(message);
    
    // Create a temporary div to parse HTML
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = formattedMessage;
    const textContent = tempDiv.textContent || tempDiv.innerText;
    
    element.textContent = "";
    
    function type() {
        if (index < textContent.length) {
            element.textContent += textContent.charAt(index);
            index++;
            scrollToBottom();
            setTimeout(type, speed);
        } else {
            // Replace with formatted HTML after typing is complete
            element.innerHTML = formattedMessage;
        }
    }
    
    type();
}

// Format message to handle line breaks and preserve formatting
function formatMessage(message) {
    return message
        .replace(/\n/g, '<br>')
        .replace(/•/g, '<span style="margin-right: 8px;">•</span>');
}

// Show typing indicator
function showTypingIndicator() {
    const chatContainer = document.querySelector(".chatcontent > div");
    const typingIndicator = document.createElement("div");
    
    typingIndicator.classList.add("messages__item", "messages__item--visitor", "typing-indicator");
    typingIndicator.id = "typing-indicator";
    typingIndicator.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    chatContainer.appendChild(typingIndicator);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById("typing-indicator");
    if (typingIndicator) {
        typingIndicator.style.opacity = "0";
        setTimeout(() => {
            typingIndicator.remove();
        }, 300);
    }
}

// Smooth scroll to bottom
function scrollToBottom() {
    const chatContainer = document.querySelector(".chatcontent > div");
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

// ---------------------------
// Navigation Toggle (Mobile)
// ---------------------------
function initNavToggle() {
    const toggleBtn = document.getElementById("navToggle");
    const navPane = document.querySelector(".navipane");

    if (!toggleBtn || !navPane) return; // Safety check

    toggleBtn.addEventListener("click", () => {
        navPane.classList.toggle("open");
    });
}

// ---------------------------
// Page Initialization
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Show greeting with typing effect
    setTimeout(() => {
        addMessageWithTyping("Tibby", "👋 Hello, Gentinian! I am Tibby, GTDLNHS' cutest chatbot. How may I help you today?");
    }, 500);

    // Enable Enter key to send
    const input = document.getElementById("query");
    input.addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Init mobile navigation toggle
    initNavToggle();
});