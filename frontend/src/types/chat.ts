export interface Message {
  id: string
  content: string
  type: 'user' | 'bot'
  timestamp: Date
  intent?: string
  confidence?: number
  responseTime?: number
  provider?: string
  sources?: string[]
}

export interface ChatResponse {
  response: string
  intent: string
  confidence: number
  response_time_ms: number
  provider: string
  sources?: string[]
}

export interface GreetingResponse {
  message: string
  provider: string
}

export interface HealthResponse {
  status: string
  providers: {
    chat: {
      active: string
      available: string[]
    }
    embeddings: {
      active: string
      available: string[]
    }
  }
}
