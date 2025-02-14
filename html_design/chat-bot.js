document
.getElementById("send-btn")
.addEventListener("click", function () {
  const userInput = document.getElementById("user-input").value.trim();
  if (userInput === "") return;

  const chatBox = document.getElementById("chat-box");
  const userMessage = `<div class='message user'>${userInput}</div>`;
  chatBox.innerHTML += userMessage;

  setTimeout(() => {
    const botResponse =
      "<div class='message bot'>This is a artificial response.</div>";
    chatBox.innerHTML += botResponse;
    chatBox.scrollTop = chatBox.scrollHeight;
  }, 500);

  document.getElementById("user-input").value = "";
});

