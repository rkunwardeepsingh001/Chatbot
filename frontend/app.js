const { useState, useEffect, useRef } = React;

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cardActive, setCardActive] = useState(false);
  const [chatVisible, setChatVisible] = useState(false);
  const bottomRef = useRef(null);
  const chatRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const nextMessages = [...messages, { role: 'user', text: trimmed }];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: trimmed })
      });

      let data;
      const contentType = response.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        data = await response.json();
      } else {
        const text = await response.text();
        data = {
          error: text.includes('<!DOCTYPE') ? 'Server returned an unexpected HTML error page.' : text || 'Unexpected server response'
        };
      }

      if (!response.ok) {
        throw new Error(data.error || `Server error ${response.status}`);
      }

      setMessages(prev => [...prev, { role: 'bot', text: data.bot }]);
    } catch (err) {
      setError(err.message);
      setMessages(prev => [...prev, { role: 'bot', text: 'Sorry, something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = event => {
    event.preventDefault();
    sendMessage();
  };

  const toggleChat = () => {
    setChatVisible(prev => {
      const next = !prev;
      if (next) {
        if (chatRef.current) {
          chatRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        if (inputRef.current) {
          inputRef.current.focus();
        }
        setCardActive(true);
        setTimeout(() => setCardActive(false), 1200);
      }
      return next;
    });
  };

  return React.createElement(
    'div',
    { className: 'app-shell' },
    React.createElement('button', { className: 'top-right-bg-btn', type: 'button', onClick: toggleChat }, chatVisible ? 'Close AI' : 'Chat AI'),
    React.createElement(
      'div',
      { className: 'bg-scene' },
      React.createElement('div', { className: 'bg-orb orb-1' }),
      React.createElement('div', { className: 'bg-orb orb-2' }),
      React.createElement('div', { className: 'bg-ring ring-1' }),
      React.createElement('div', { className: 'bg-ring ring-2' }),
      React.createElement('div', { className: 'bg-panel' })
    ),
    React.createElement(
      'div',
      { className: `chat-card${cardActive ? ' active' : ''}${chatVisible ? ' visible' : ' hidden'}`, ref: chatRef },
      React.createElement(
        'header',
        { className: 'chat-header' },
        React.createElement('div', null,
          React.createElement('h1', null, 'Chatbot UI'),
          React.createElement('p', null, 'Send a message and get a response from your Django chatbot API.')
        ),
        React.createElement('button', { className: 'top-action-btn', type: 'button', onClick: toggleChat }, chatVisible ? 'Close' : 'Chat AI')
      ),
      React.createElement(
        'div',
        { className: 'chat-window' },
        messages.length === 0 && React.createElement('div', { className: 'chat-empty' }, 'Type a message and press Enter to start the conversation.'),
        messages.map((message, index) => React.createElement(
          'div',
          {
            key: index,
            className: `chat-message ${message.role === 'user' ? 'user' : 'bot'}`
          },
          React.createElement('span', null, message.text)
        )),
        React.createElement('div', { ref: bottomRef })
      ),
      React.createElement(
        'form',
        { className: 'chat-input-form', onSubmit: handleSubmit },
        React.createElement('input', {
          ref: inputRef,
          value: input,
          onChange: e => setInput(e.target.value),
          placeholder: 'Write your message...',
          disabled: loading
        }),
        React.createElement('button', { type: 'submit', disabled: loading }, loading ? 'Sending...' : 'Send')
      ),
      error && React.createElement('div', { className: 'chat-error' }, error)
    )
  );
}

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);
root.render(React.createElement(App));
