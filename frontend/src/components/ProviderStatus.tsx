import React from 'react'
import { Zap, Cpu, Wifi, AlertCircle } from 'lucide-react'

interface ProviderStatusProps {
  provider?: string
  responseTime?: number
  isConnected: boolean
}

const ProviderStatus: React.FC<ProviderStatusProps> = ({ 
  provider, 
  responseTime, 
  isConnected 
}) => {
  const getProviderIcon = (provider?: string) => {
    if (provider?.includes('OpenAI')) return '🤖'
    if (provider?.includes('HuggingFace')) return '🤗'
    if (provider?.includes('Intent-based')) return '📝'
    if (provider?.includes('Ollama')) return '🦙'
    return '❓'
  }

  const getProviderLabel = (provider?: string) => {
    if (provider?.includes('OpenAI')) return 'OpenAI API'
    if (provider?.includes('HuggingFace')) return 'HuggingFace API'
    if (provider?.includes('Intent-based')) return 'Intent Fallback'
    if (provider?.includes('Ollama')) return 'Ollama Local'
    return provider || 'Unknown'
  }

  const getProviderColor = (provider?: string) => {
    if (provider?.includes('OpenAI')) return 'text-green-600 bg-green-50 border-green-200'
    if (provider?.includes('HuggingFace')) return 'text-blue-600 bg-blue-50 border-blue-200'
    if (provider?.includes('Intent-based')) return 'text-purple-600 bg-purple-50 border-purple-200'
    if (provider?.includes('Ollama')) return 'text-orange-600 bg-orange-50 border-orange-200'
    return 'text-gray-600 bg-gray-50 border-gray-200'
  }

  const getResponseTimeColor = (time?: number) => {
    if (!time) return 'text-gray-500'
    if (time < 1000) return 'text-green-500'
    if (time < 5000) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getResponseTimeLabel = (time?: number) => {
    if (!time) return 'Unknown'
    if (time < 1000) return 'Fast'
    if (time < 5000) return 'Normal'
    return 'Slow'
  }

  return (
    <div className="flex items-center space-x-3 p-3 bg-white rounded-lg border border-gray-200 shadow-sm">
      {/* Connection Status */}
      <div className="flex items-center space-x-2">
        <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
        <span className="text-xs text-gray-600">
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>

      {/* Provider Information */}
      {provider && (
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full border ${getProviderColor(provider)}`}>
          <span className="text-sm">{getProviderIcon(provider)}</span>
          <span className="text-xs font-medium">{getProviderLabel(provider)}</span>
        </div>
      )}

      {/* Response Time */}
      {responseTime && (
        <div className="flex items-center space-x-1">
          <Zap className="w-3 h-3 text-gray-400" />
          <span className={`text-xs font-medium ${getResponseTimeColor(responseTime)}`}>
            {responseTime}ms ({getResponseTimeLabel(responseTime)})
          </span>
        </div>
      )}

      {/* Provider Type Indicator */}
      {provider?.includes('Intent-based') && (
        <div className="flex items-center space-x-1 text-purple-600">
          <AlertCircle className="w-3 h-3" />
          <span className="text-xs">Fallback Mode</span>
        </div>
      )}
    </div>
  )
}

export default ProviderStatus
