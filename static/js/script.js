let userMessages = [];
let botMessages = [];
const msgContainer = document.getElementById("msgContainer");
const botGreeting = "Esawi online. How may I assist you today?";

// Show the messages in the chat container
function showMessages() {
  msgContainer.innerHTML = "";

  const initialGreeting = createBotMessage(botGreeting);
  initialGreeting.classList.add("hidden");
  msgContainer.appendChild(initialGreeting);

  userMessages.forEach((userMessage, index) => {
    const userDiv = createUserMessage(userMessage);
    userDiv.classList.add("hidden");
    msgContainer.appendChild(userDiv);

    if (botMessages[index]) {
      const botDiv = createBotMessage(botMessages[index]);
      botDiv.classList.add("hidden");
      msgContainer.appendChild(botDiv);
    }
  });

  requestAnimationFrame(() => {
    const messages = msgContainer.querySelectorAll(".chat-bubble");
    messages.forEach((message, index) => {
      setTimeout(() => {
        const zTranslate = Math.random() * 20;
        const yRotate = Math.random() * 10 - 5;
        message.style.transition = "all 0.5s ease-out";
        message.style.transform = `translateZ(${zTranslate}px) rotateY(${yRotate}deg)`;
        message.style.opacity = "0";

        requestAnimationFrame(() => {
          message.classList.remove("hidden");
          message.style.transform = "translateZ(0) rotateY(0)";
          message.style.opacity = "1";
        });
      }, index * 200);
    });
  });

  msgContainer.scrollTop = msgContainer.scrollHeight;
}

// Create user message bubble
function createUserMessage(message) {
  const div = document.createElement("div");
  div.className = "chat-bubble user hidden";
  div.textContent = message;
  return div;
}

// Create bot message bubble
function createBotMessage(message) {
  const div = document.createElement("div");
  div.className = "chat-bubble bot hidden";
  // Use marked.js to parse and render Markdown
  div.innerHTML = marked.parse(message);
  return div;
}

// Handle input event for styling input wrapper
function onInput(event) {
  const input = event.target.value;
  const inputWrapper = event.target.closest(".input-wrapper");
  if (input.trim() !== "") {
    inputWrapper.style.borderColor = "rgba(0, 255, 255, 0.6)";
    inputWrapper.style.boxShadow = "0 0 10px rgba(0, 255, 255, 0.3)";
  } else {
    inputWrapper.style.borderColor = "rgba(0, 255, 255, 0.2)";
    inputWrapper.style.boxShadow = "none";
  }
}

// Display thinking message
function showBotThinking() {
  const thinkingMessage = createBotMessage("Bot is thinking...");
  msgContainer.appendChild(thinkingMessage);
  msgContainer.scrollTop = msgContainer.scrollHeight;
}

// Handle the click event when sending a message
async function onClick(event) {
  if (event) event.preventDefault(); // Prevent form submission if triggered by a form

  const inputField = document.getElementById("chatInput");
  const inputValue = inputField.value.trim();

  if (inputValue === "") return;

  userMessages.push(inputValue);
  showMessages(); // Display user message immediately

  showBotThinking(); // Show bot is thinking

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: inputValue }),
    });

    const data = await response.json();

    if (data.response) {
      botMessages.push(data.response);
    } else {
      botMessages.push(
        "Sorry, I couldn't process your request. Please try again."
      );
    }

    inputField.value = "";
    showMessages();
  } catch (error) {
    console.error("Error:", error);
    botMessages.push("An error occurred. Please try again later.");
    showMessages();
  }
}

// Add CSS for hidden state and thinking animation
const style = document.createElement("style");
style.textContent = `
  .chat-bubble.hidden {
    opacity: 0;
    transform: translateZ(20px) rotateY(-5deg);
  }
  .chat-bubble.bot {
    background-color: #f1f1f1;
    color: #333;
  }
  .chat-bubble.user {
    background-color: #0b7dda;
    color: white;
  }
  .chat-bubble.bot:after {
    content: "";
    font-size: 1.5em;
    display: block;
    text-align: center;
  }
`;
document.head.appendChild(style);

// Add event listeners on DOM content load
document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("chatInput");
  const sendButton = document.getElementById("sendButton");

  inputField.addEventListener("input", onInput);

  sendButton.addEventListener("click", onClick);

  // Allow sending message with Enter key
  inputField.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent default form submission
      onClick();
    }
  });

  showMessages();
});
