import { useState, useRef, useEffect } from 'react'
import { streamChat } from '@/services/api'

interface Message {
  role: 'user' | 'assistant'
  content: string
  tools?: any[]
}

interface ChatInterfaceProps {
  onToolCall?: (tool: any) => void
}

export default function ChatInterface({ onToolCall }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      let assistantMessage = ''
      let tools: any[] = []

      await streamChat(input, {
        onToken: (token) => {
          assistantMessage += token
          setMessages(prev => {
            const newMessages = [...prev]
            if (newMessages[newMessages.length - 1]?.role === 'assistant') {
              newMessages[newMessages.length - 1].content = assistantMessage
            } else {
              newMessages.push({ role: 'assistant', content: assistantMessage })
            }
            return newMessages
          })
        },
        onTools: (toolCalls) => {
          tools = toolCalls
          if (onToolCall && toolCalls.length > 0) {
            onToolCall(toolCalls[toolCalls.length - 1])
          }
          setMessages(prev => {
            const newMessages = [...prev]
            if (newMessages[newMessages.length - 1]?.role === 'assistant') {
              newMessages[newMessages.length - 1].tools = toolCalls
            }
            return newMessages
          })
        },
        onError: (error) => {
          console.error('Stream error:', error)
          setMessages(prev => [...prev, { 
            role: 'assistant', 
            content: 'Error: Failed to get response' 
          }])
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl flex flex-col h-[600px]">
      {/* Header */}
      <div className="bg-gray-700 px-6 py-4 rounded-t-lg">
        <h2 className="text-xl font-semibold text-white">Chat</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">Start a conversation with the AI agent</p>
            <p className="text-sm mt-2">Try asking questions or requesting calculations</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                {message.tools && message.tools.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-gray-600">
                    <p className="text-xs text-gray-300">
                      Tools used: {message.tools.map(t => t.name).join(', ')}
                    </p>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={loading}
            className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  )
}
