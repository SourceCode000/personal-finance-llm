// frontend/app.js

const API_URL = "http://localhost:8000/chat"

// This is our entire "database" for now
// Lives in memory, gone on refresh
let messages = []

// Show welcome message on load
window.onload = () => {
  addMessageToUI("assistant",
    "Hi! I'm your personal finance assistant. " +
    "What's on your mind — budgeting, saving, debt, " +
    "or something else?"
  )
}

async function sendMessage() {
  const input = document.getElementById("input")
  const text = input.value.trim()
  if (!text) return

  // Clear input, disable button
  input.value = ""
  setLoading(true)

  // Add user message to UI and history
  addMessageToUI("user", text)
  messages.push({ role: "user", content: text })

  // Show typing indicator
  const loadingId = addMessageToUI("assistant", "typing...", true)

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages })
    })

    const data = await res.json()
    const reply = data.response

    // Replace loading with real response
    removeMessage(loadingId)
    addMessageToUI("assistant", reply)

    // Add to history
    messages.push({ role: "assistant", content: reply })

  } catch (err) {
    removeMessage(loadingId)
    addMessageToUI("assistant",
      "Sorry, something went wrong. Please try again."
    )
  }

  setLoading(false)
}

function addMessageToUI(role, content, isLoading = false) {
  const messagesDiv = document.getElementById("messages")
  const id = "msg_" + Date.now()

  const div = document.createElement("div")
  div.className = `message ${isLoading ? "loading" : role}`
  div.id = id
  div.textContent = content

  messagesDiv.appendChild(div)
  messagesDiv.scrollTop = messagesDiv.scrollHeight

  return id
}

function removeMessage(id) {
  const el = document.getElementById(id)
  if (el) el.remove()
}

function setLoading(isLoading) {
  const btn = document.getElementById("send-btn")
  const input = document.getElementById("input")
  btn.disabled = isLoading
  input.disabled = isLoading
}

function handleKey(event) {
  if (event.key === "Enter") sendMessage()
}