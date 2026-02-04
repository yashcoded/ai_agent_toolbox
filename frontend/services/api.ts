/**
 * API service for communicating with the backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface StreamCallbacks {
  onToken?: (token: string) => void
  onTools?: (tools: any[]) => void
  onError?: (error: string) => void
  onComplete?: () => void
}

/**
 * Stream chat messages using Server-Sent Events (SSE)
 */
export async function streamChat(message: string, callbacks: StreamCallbacks) {
  const sessionId = getOrCreateSessionId()

  try {
    const response = await fetch(`${API_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body?.getReader()
    if (!reader) throw new Error('No reader available')

    const decoder = new TextDecoder()
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6))
            
            if (data.type === 'token' && callbacks.onToken) {
              callbacks.onToken(data.content)
            } else if (data.type === 'tools' && callbacks.onTools) {
              callbacks.onTools(data.tools)
            } else if (data.type === 'error' && callbacks.onError) {
              callbacks.onError(data.message)
            } else if (data.type === 'end' && callbacks.onComplete) {
              callbacks.onComplete()
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e)
          }
        }
      }
    }
  } catch (error) {
    console.error('Stream error:', error)
    if (callbacks.onError) {
      callbacks.onError(error instanceof Error ? error.message : 'Unknown error')
    }
  }
}

/**
 * Run a specific tool
 */
export async function runTool(toolName: string, parameters: Record<string, any>) {
  const response = await fetch(`${API_URL}/tools/run`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tool_name: toolName,
      parameters,
    }),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return response.json()
}

/**
 * Get evaluations
 */
export async function getEvaluations(limit: number = 100) {
  const response = await fetch(`${API_URL}/evals?limit=${limit}`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return response.json()
}

/**
 * Get or create a session ID
 */
function getOrCreateSessionId(): string {
  let sessionId = localStorage.getItem('session_id')
  
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2, 11)}`
    localStorage.setItem('session_id', sessionId)
  }
  
  return sessionId
}
