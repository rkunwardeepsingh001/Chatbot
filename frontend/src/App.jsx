import { useEffect, useRef, useState } from 'react'

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    const trimmed = input.trim()
    if (!trimmed) return

    const nextMessages = [...messages, { role: 'user', text: trimmed }]
    setMessages(nextMessages)
    setInput('')
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: trimmed })
      })

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Unable to get response')
      }

      setMessages(prev => [...prev, { role: 'bot', text: data.bot }])
    } catch (err) {
      setError(err.message)
      setMessages(prev => [...prev, { role: 'bot', text: 'Sorry, something went wrong.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = event => {
    event.preventDefault()
    sendMessage()
  }

  return (
    <div className="app-shell">
      <div className="chat-card">
        <header className="chat-header">
          <div>
            <h1>Chatbot UI</h1>
            <p>Send a message and get a response from your Django chatbot API.</p>
          </div>
        </header>

        <div className="chat-window">
          {messages.length === 0 && (
            <div className="chat-empty">Type a message and press Enter to start the conversation.</div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat-message ${message.role === 'user' ? 'user' : 'bot'}`}
            >
              <span>{message.text}</span>
            </div>
          ))}

          <div ref={bottomRef} />
        </div>

        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Write your message..."
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>

        {error && <div className="chat-error">{error}</div>}
      </div>
    </div>
  )
}

export default App
