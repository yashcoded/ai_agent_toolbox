import { useEffect, useState } from 'react'

interface Tool {
  name: string
  input: string
  output?: string
  status: string
}

interface ToolVisualizerProps {
  activeTool?: Tool | null
}

export default function ToolVisualizer({ activeTool }: ToolVisualizerProps) {
  const [tools, setTools] = useState<any[]>([])

  useEffect(() => {
    fetchTools()
  }, [])

  const fetchTools = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/tools`)
      const data = await response.json()
      setTools(data.tools)
    } catch (error) {
      console.error('Error fetching tools:', error)
    }
  }

  return (
    <div className="bg-gray-800 rounded-lg shadow-xl p-6 h-[600px] flex flex-col">
      <h2 className="text-xl font-semibold text-white mb-4">Tools</h2>

      {/* Available Tools */}
      <div className="space-y-3 mb-6">
        {tools.map((tool) => (
          <div
            key={tool.name}
            className="bg-gray-700 rounded-lg p-3 border border-gray-600"
          >
            <h3 className="font-medium text-white">{tool.name}</h3>
            <p className="text-sm text-gray-400 mt-1">{tool.description}</p>
          </div>
        ))}
      </div>

      {/* Active Tool */}
      {activeTool && (
        <div className="mt-auto">
          <h3 className="text-lg font-semibold text-white mb-3">Active Tool</h3>
          <div className="bg-gray-700 rounded-lg p-4 border-2 border-blue-500">
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-medium text-white">{activeTool.name}</h4>
              <span className={`px-2 py-1 rounded text-xs ${
                activeTool.status === 'completed'
                  ? 'bg-green-900 text-green-200'
                  : 'bg-yellow-900 text-yellow-200'
              }`}>
                {activeTool.status}
              </span>
            </div>
            <div className="text-sm text-gray-400 mt-2">
              <p><strong>Input:</strong> {activeTool.input}</p>
              {activeTool.output && (
                <p className="mt-1"><strong>Output:</strong> {activeTool.output}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
