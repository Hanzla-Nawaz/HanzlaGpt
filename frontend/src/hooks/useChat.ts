import { useState, useEffect, useCallback } from 'react'
import { Message, ChatResponse, GreetingResponse, HealthResponse } from '../types/chat'
import toast from 'react-hot-toast'

// In production (on Vercel), use same-origin relative path and let Vercel proxy to the backend.
// In development, use explicit URL if provided, else localhost.
const API_BASE_URL = import.meta.env.PROD ? '' : (import.meta.env.VITE_API_URL || 'http://localhost:8000')

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [greeting, setGreeting] = useState<string | null>(null)
  const [provider, setProvider] = useState<string | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  const checkHealth = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/health`)
      if (response.ok) {
        const data: HealthResponse = await response.json()
        setIsConnected(true)
        setProvider(data.providers.chat.active)
        return true
      }
    } catch (error) {
      console.error('Health check failed:', error)
    }
    setIsConnected(false)
    return false
  }, [])

  const loadGreeting = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/greeting`)
      if (response.ok) {
        const data: GreetingResponse = await response.json()
        setGreeting(data.message)
        setProvider(data.provider)
      }
    } catch (error) {
      console.error('Failed to load greeting:', error)
      // Fallback greeting
      setGreeting(`🤖 Welcome! I'm HanzlaGPT - Your Personal AI Assistant

Hi there! I'm Hanzala Nawaz, your AI-powered personal assistant. I'm here to help you with:

• **Career Guidance** - AI, ML, Cybersecurity career advice
• **Technical Questions** - Programming, frameworks, best practices  
• **Project Help** - Code reviews, architecture decisions
• **Learning Paths** - Skill development, certification recommendations
• **Industry Insights** - Latest trends, job market analysis

What would you like to know?`)
    }
  }, [])

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: content.trim(),
      type: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'web_user',
          session_id: 'web_session',
          query: content.trim(),
          stream: false,
        }),
      })

      if (response.status === 429) {
        const data = await response.json()
        toast.error(data.detail || 'Query limit reached.')
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: data.detail || 'You have reached the maximum number of free queries.',
          type: 'bot',
          timestamp: new Date(),
        }
        setMessages(prev => [...prev, errorMessage])
        return
      }

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data: ChatResponse = await response.json()

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        type: 'bot',
        timestamp: new Date(),
        intent: data.intent,
        confidence: data.confidence,
        responseTime: data.response_time_ms,
        provider: data.provider,
        sources: data.sources ?? [],
      }

      setMessages(prev => [...prev, botMessage])
      setProvider(data.provider)
      // Provider/API toast notifications removed

    } catch (error) {
      console.error('Failed to send message:', error)
      toast.error('Failed to send message. Please try again.')
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again or check your connection.',
        type: 'bot',
        timestamp: new Date(),
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    checkHealth()
    loadGreeting()
    
    // Periodic health check
    const interval = setInterval(checkHealth, 30000) // Every 30 seconds
    
    return () => clearInterval(interval)
  }, [checkHealth, loadGreeting])

  return {
    messages,
    isLoading,
    sendMessage,
    greeting,
    provider,
    isConnected,
  }
}
