import React from 'react'
import { User, Bot, Clock, Zap } from 'lucide-react'
import { motion } from 'framer-motion'
import { Message as MessageType } from '../types/chat'
import { format } from 'date-fns'

interface MessageProps {
  message: MessageType
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.type === 'user'
  
  const getIntentColor = (intent?: string) => {
    switch (intent) {
      case 'career_guidance':
        return 'intent-career'
      case 'ai_advice':
        return 'intent-ai'
      case 'cybersecurity_advice':
        return 'intent-cyber'
      case 'personal_info':
        return 'intent-personal'
      default:
        return 'intent-general'
    }
  }

  const getIntentLabel = (intent?: string) => {
    switch (intent) {
      case 'career_guidance':
        return 'Career'
      case 'ai_advice':
        return 'AI/ML'
      case 'cybersecurity_advice':
        return 'Security'
      case 'personal_info':
        return 'Personal'
      default:
        return 'General'
    }
  }

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

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div className={`flex items-start space-x-3 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
          isUser 
            ? 'bg-gradient-to-r from-primary-600 to-secondary-600' 
            : 'bg-gradient-to-r from-gray-600 to-gray-700'
        }`}>
          {isUser ? (
            <User className="w-4 h-4 text-white" />
          ) : (
            <Bot className="w-4 h-4 text-white" />
          )}
        </div>

        {/* Message Content */}
        <div className={`message-bubble ${isUser ? 'message-user' : 'message-bot'}`}>
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap">{message.content}</div>
          </div>
          
          {/* Message Metadata */}
          <div className={`flex items-center justify-between mt-3 text-xs ${
            isUser ? 'text-white/70' : 'text-gray-500'
          }`}>
            <div className="flex items-center space-x-2">
              <Clock className="w-3 h-3" />
              <span>{format(message.timestamp, 'HH:mm')}</span>
              
              {message.responseTime && (
                <>
                  <Zap className="w-3 h-3" />
                  <span>{message.responseTime}ms</span>
                </>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              {message.intent && (
                <span className={`intent-badge ${getIntentColor(message.intent)}`}>
                  {getIntentLabel(message.intent)}
                </span>
              )}
              
              {message.confidence && (
                <span className="text-xs opacity-70">
                  {(message.confidence * 100).toFixed(0)}%
                </span>
              )}
              
              {message.provider && (
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                  message.provider.includes('OpenAI') 
                    ? 'bg-green-100 text-green-800' 
                    : message.provider.includes('Groq')
                    ? 'bg-yellow-100 text-yellow-800'
                    : message.provider.includes('Together AI')
                    ? 'bg-indigo-100 text-indigo-800'
                    : message.provider.includes('Replicate')
                    ? 'bg-pink-100 text-pink-800'
                    : message.provider.includes('HuggingFace')
                    ? 'bg-blue-100 text-blue-800'
                    : message.provider.includes('Intent-based')
                    ? 'bg-purple-100 text-purple-800'
                    : message.provider.includes('Ollama')
                    ? 'bg-orange-100 text-orange-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                  {getProviderIcon(message.provider)} {getProviderLabel(message.provider)}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default Message
