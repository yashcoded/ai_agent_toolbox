import { useState } from 'react'
import Head from 'next/head'
import ChatInterface from '@/components/ChatInterface'
import ToolVisualizer from '@/components/ToolVisualizer'

export default function Home() {
  const [activeTool, setActiveTool] = useState<any>(null)

  return (
    <>
      <Head>
        <title>AI Agent Toolbox</title>
        <meta name="description" content="AI Agent with tool calling capabilities" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            AI Agent Toolbox
          </h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <ChatInterface onToolCall={setActiveTool} />
            </div>
            <div>
              <ToolVisualizer activeTool={activeTool} />
            </div>
          </div>
        </div>
      </main>
    </>
  )
}
