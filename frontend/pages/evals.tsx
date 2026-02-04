import { useState, useEffect } from 'react'
import Head from 'next/head'

interface Evaluation {
  id: number
  test_name: string
  passed: boolean
  score: number
  created_at: string
}

export default function Evals() {
  const [evaluations, setEvaluations] = useState<Evaluation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchEvaluations()
  }, [])

  const fetchEvaluations = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/evals`)
      const data = await response.json()
      setEvaluations(data.evaluations)
    } catch (error) {
      console.error('Error fetching evaluations:', error)
    } finally {
      setLoading(false)
    }
  }

  const passRate = evaluations.length > 0
    ? (evaluations.filter(e => e.passed).length / evaluations.length * 100).toFixed(1)
    : 0

  const avgScore = evaluations.length > 0
    ? (evaluations.reduce((sum, e) => sum + e.score, 0) / evaluations.length).toFixed(2)
    : 0

  return (
    <>
      <Head>
        <title>Evaluations Dashboard - AI Agent Toolbox</title>
      </Head>
      <main className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8">Evaluations Dashboard</h1>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-gray-400 text-sm mb-2">Total Tests</h3>
              <p className="text-3xl font-bold">{evaluations.length}</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-gray-400 text-sm mb-2">Pass Rate</h3>
              <p className="text-3xl font-bold">{passRate}%</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-gray-400 text-sm mb-2">Average Score</h3>
              <p className="text-3xl font-bold">{avgScore}</p>
            </div>
          </div>

          {/* Evaluations Table */}
          <div className="bg-gray-800 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Test Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-4 text-center">
                      Loading...
                    </td>
                  </tr>
                ) : evaluations.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-6 py-4 text-center text-gray-400">
                      No evaluations yet
                    </td>
                  </tr>
                ) : (
                  evaluations.map((eval) => (
                    <tr key={eval.id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {eval.test_name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 rounded text-xs ${
                          eval.passed 
                            ? 'bg-green-900 text-green-200' 
                            : 'bg-red-900 text-red-200'
                        }`}>
                          {eval.passed ? 'PASS' : 'FAIL'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {(eval.score * 100).toFixed(0)}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-gray-400">
                        {new Date(eval.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </>
  )
}
