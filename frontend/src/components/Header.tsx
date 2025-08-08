import React from 'react'
import { Bot, Zap, Shield, Code, Brain } from 'lucide-react'

const Header: React.FC = () => {
  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-sm">HN</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gradient">Hanzla Nawaz</h1>
                <p className="text-sm text-gray-600">AI Engineer & Cybersecurity Analyst</p>
              </div>
            </div>
            <div className="flex items-center space-x-1 ml-4">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-500">Live</span>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Brain className="w-4 h-4" />
              <span>AI & ML</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Shield className="w-4 h-4" />
              <span>Cybersecurity</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Code className="w-4 h-4" />
              <span>Development</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Zap className="w-4 h-4" />
              <span>Career Guidance</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
