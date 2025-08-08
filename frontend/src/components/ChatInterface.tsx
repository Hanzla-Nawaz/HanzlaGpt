import React, { useState, useEffect, useRef } from 'react'
import { Send, Loader2, Bot, User, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import toast from 'react-hot-toast'
import Message from './Message'
import GreetingMessage from './GreetingMessage'
import ProviderStatus from './ProviderStatus'
import { useChat } from '../hooks/useChat'

const ChatInterface: React.FC = () => {
  const {
    messages,
    isLoading,
    sendMessage,
    greeting,
    provider,
    isConnected
  } = useChat()

  const getProviderIcon = (provider?: string) => {
    if (provider?.includes('OpenAI')) return '🤖'
    if (provider?.includes('Groq')) return '⚡'
    if (provider?.includes('Together AI')) return '🤝'
    if (provider?.includes('Replicate')) return '🔄'
    if (provider?.includes('HuggingFace')) return '🤗'
    if (provider?.includes('Intent-based')) return '📝'
    if (provider?.includes('Ollama')) return '🦙'
    return '❓'
  }

  const getProviderLabel = (provider?: string) => {
    if (provider?.includes('OpenAI')) return 'OpenAI'
    if (provider?.includes('Groq')) return 'Groq'
    if (provider?.includes('Together AI')) return 'Together AI'
    if (provider?.includes('Replicate')) return 'Replicate'
    if (provider?.includes('HuggingFace')) return 'HuggingFace'
    if (provider?.includes('Intent-based')) return 'Fallback'
    if (provider?.includes('Ollama')) return 'Ollama'
    return provider || 'Unknown'
  }

  const getProviderDescription = (provider?: string) => {
    if (provider?.includes('OpenAI')) return 'Premium AI Service'
    if (provider?.includes('Groq')) return 'Ultra-Fast AI (1000/day free)'
    if (provider?.includes('Together AI')) return 'Reliable AI (1000/day free)'
    if (provider?.includes('Replicate')) return 'High-Quality AI (500/day free)'
    if (provider?.includes('HuggingFace')) return 'Open-Source AI (30K/month free)'
    if (provider?.includes('Intent-based')) return 'Local Fallback (No API needed)'
    if (provider?.includes('Ollama')) return 'Local AI (Unlimited)'
    return 'AI Service'
  }

  const [inputValue, setInputValue] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const message = inputValue.trim()
    setInputValue('')
    
    try {
      await sendMessage(message)
    } catch (error) {
      toast.error('Failed to send message. Please try again.')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="card h-[600px] flex flex-col">
        {/* Chat Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">HanzlaGPT</h2>
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className="text-sm text-gray-500">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
                {provider && (
                  <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                    provider.includes('OpenAI') 
                      ? 'bg-green-100 text-green-800' 
                      : provider.includes('Groq')
                      ? 'bg-yellow-100 text-yellow-800'
                      : provider.includes('Together AI')
                      ? 'bg-indigo-100 text-indigo-800'
                      : provider.includes('Replicate')
                      ? 'bg-pink-100 text-pink-800'
                      : provider.includes('HuggingFace')
                      ? 'bg-blue-100 text-blue-800'
                      : provider.includes('Intent-based')
                      ? 'bg-purple-100 text-purple-800'
                      : provider.includes('Ollama')
                      ? 'bg-orange-100 text-orange-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {getProviderIcon(provider)} {getProviderLabel(provider)}
                  </span>
                )}
              </div>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Sparkles className="w-4 h-4" />
            <span>AI Assistant</span>
          </div>
        </div>

        {/* Provider Status Bar */}
        <div className="px-6 py-2 bg-gray-50 border-b border-gray-100">
          <ProviderStatus 
            provider={provider || undefined}
            responseTime={messages.length > 0 ? messages[messages.length - 1]?.responseTime : undefined}
            isConnected={isConnected}
          />
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {greeting && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <GreetingMessage message={greeting} provider={provider} />
              </motion.div>
            )}
            
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ delay: index * 0.1 }}
              >
                <Message message={message} />
              </motion.div>
            ))}
            
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center space-x-3 text-gray-500"
              >
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>HanzlaGPT is thinking...</span>
              </motion.div>
            )}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="p-6 border-t border-gray-100">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask HanzlaGPT anything..."
                className="input-field pr-12"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 text-gray-400 hover:text-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ChatInterface
