import React from 'react'
import { Bot, Sparkles, Brain, Shield, Code, Zap } from 'lucide-react'
import { motion } from 'framer-motion'

interface GreetingMessageProps {
  message: string
}

const GreetingMessage: React.FC<GreetingMessageProps> = ({ message }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-gradient-to-r from-primary-50 to-secondary-50 border-2 border-primary-200 rounded-2xl p-6 shadow-lg"
    >
      <div className="flex items-start space-x-4">
        <div className="w-12 h-12 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-full flex items-center justify-center flex-shrink-0">
          <Bot className="w-6 h-6 text-white" />
        </div>
        
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-3">
            <h3 className="text-lg font-semibold text-primary-700">
              Welcome to InsightAI!
            </h3>
            <Sparkles className="w-5 h-5 text-secondary-500" />
          </div>
          
          <div className="prose prose-sm max-w-none text-gray-700">
            <div className="whitespace-pre-wrap mb-4">{message}</div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4">
              <div className="flex items-center space-x-2 text-sm">
                <Brain className="w-4 h-4 text-purple-500" />
                <span>AI & Machine Learning</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <Shield className="w-4 h-4 text-orange-500" />
                <span>Cybersecurity</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <Code className="w-4 h-4 text-blue-500" />
                <span>Software Development</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <Zap className="w-4 h-4 text-green-500" />
                <span>Career Guidance</span>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-white rounded-lg border border-gray-200">
              <p className="text-sm text-gray-600 mb-2">
                <strong>💡 Pro Tips:</strong>
              </p>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• Ask about my experience in AI/ML and cybersecurity</li>
                <li>• Get career advice for tech professionals</li>
                <li>• Discuss latest industry trends and technologies</li>
                <li>• Get help with coding and project architecture</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default GreetingMessage
