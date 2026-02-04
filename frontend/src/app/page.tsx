'use client';

import { useState } from 'react';
import ChatInterface from '@/components/ChatInterface';
import ToolVisualizer from '@/components/ToolVisualizer';
import EvalDashboard from '@/components/EvalDashboard';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'tools' | 'evals'>('chat');

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Agent Toolbox
          </h1>
          <p className="text-gray-600">
            LangChain-powered agent system with streaming, tools, and observability
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'chat'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Chat
          </button>
          <button
            onClick={() => setActiveTab('tools')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'tools'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Tools
          </button>
          <button
            onClick={() => setActiveTab('evals')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'evals'
                ? 'border-b-2 border-blue-600 text-blue-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Evaluations
          </button>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          {activeTab === 'chat' && <ChatInterface />}
          {activeTab === 'tools' && <ToolVisualizer />}
          {activeTab === 'evals' && <EvalDashboard />}
        </div>
      </div>
    </main>
  );
}
