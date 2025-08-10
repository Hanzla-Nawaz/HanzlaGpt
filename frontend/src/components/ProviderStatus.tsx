import React from 'react'
import { Zap } from 'lucide-react'

interface ProviderStatusProps {
  responseTime?: number
  isConnected: boolean
}

const ProviderStatus: React.FC<ProviderStatusProps> = ({ 
  responseTime, 
  isConnected 
}) => {
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

      {/* Response Time */}
      {responseTime && (
        <div className="flex items-center space-x-1">
          <Zap className="w-3 h-3 text-gray-400" />
          <span className={`text-xs font-medium ${getResponseTimeColor(responseTime)}`}>
            {responseTime}ms ({getResponseTimeLabel(responseTime)})
          </span>
        </div>
      )}
    </div>
  )
}

export default ProviderStatus
