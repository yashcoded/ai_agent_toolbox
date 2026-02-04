'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { CheckCircle, XCircle, RefreshCw } from 'lucide-react';

interface EvalHistory {
  id: number;
  eval_name: string;
  agent_type: string;
  score: number;
  passed: boolean;
  created_at: string;
}

interface Metrics {
  total_runs: number;
  average_duration_ms: number;
  total_tool_calls: number;
  total_evaluations: number;
  average_eval_score: number;
}

export default function EvalDashboard() {
  const [evalHistory, setEvalHistory] = useState<EvalHistory[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [historyResponse, metricsResponse] = await Promise.all([
        axios.get('http://localhost:8000/api/evals/history'),
        axios.get('http://localhost:8000/api/metrics/overview'),
      ]);
      setEvalHistory(historyResponse.data);
      setMetrics(metricsResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Prepare chart data
  const chartData = evalHistory.reduce((acc: any[], eval) => {
    const existing = acc.find((item) => item.name === eval.eval_name);
    if (existing) {
      existing.passed += eval.passed ? 1 : 0;
      existing.failed += eval.passed ? 0 : 1;
    } else {
      acc.push({
        name: eval.eval_name,
        passed: eval.passed ? 1 : 0,
        failed: eval.passed ? 0 : 1,
      });
    }
    return acc;
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Evaluation Dashboard</h2>
        <button
          onClick={fetchData}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">
          <p className="text-gray-500">Loading dashboard...</p>
        </div>
      ) : (
        <>
          {/* Metrics Cards */}
          {metrics && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
              <div className="bg-blue-50 rounded-lg p-4">
                <p className="text-sm text-blue-600 font-medium">Total Runs</p>
                <p className="text-2xl font-bold text-blue-900 mt-1">
                  {metrics.total_runs}
                </p>
              </div>
              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-green-600 font-medium">Avg Duration</p>
                <p className="text-2xl font-bold text-green-900 mt-1">
                  {Math.round(metrics.average_duration_ms)}ms
                </p>
              </div>
              <div className="bg-purple-50 rounded-lg p-4">
                <p className="text-sm text-purple-600 font-medium">Tool Calls</p>
                <p className="text-2xl font-bold text-purple-900 mt-1">
                  {metrics.total_tool_calls}
                </p>
              </div>
              <div className="bg-orange-50 rounded-lg p-4">
                <p className="text-sm text-orange-600 font-medium">Evaluations</p>
                <p className="text-2xl font-bold text-orange-900 mt-1">
                  {metrics.total_evaluations}
                </p>
              </div>
              <div className="bg-pink-50 rounded-lg p-4">
                <p className="text-sm text-pink-600 font-medium">Avg Score</p>
                <p className="text-2xl font-bold text-pink-900 mt-1">
                  {(metrics.average_eval_score * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          )}

          {/* Chart */}
          {chartData.length > 0 && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Evaluation Results by Test
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="passed" fill="#10b981" name="Passed" />
                  <Bar dataKey="failed" fill="#ef4444" name="Failed" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Recent Evaluations */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Recent Evaluations
            </h3>
            <div className="space-y-2">
              {evalHistory.map((eval) => (
                <div
                  key={eval.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    {eval.passed ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600" />
                    )}
                    <div>
                      <p className="font-medium text-gray-900">{eval.eval_name}</p>
                      <p className="text-sm text-gray-600">
                        {eval.agent_type} • Score: {(eval.score * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-500">
                    {new Date(eval.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {evalHistory.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500">No evaluation history available</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
