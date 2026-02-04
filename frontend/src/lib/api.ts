/**
 * API client utilities for communicating with the backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Agent API
export const agentAPI = {
  run: async (query: string, agentType: 'research' | 'code') => {
    const response = await apiClient.post('/api/agents/run', {
      query,
      agent_type: agentType,
      stream: false,
    });
    return response.data;
  },

  getHistory: async (limit: number = 10, agentType?: string) => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (agentType) params.append('agent_type', agentType);
    const response = await apiClient.get(`/api/agents/history?${params}`);
    return response.data;
  },
};

// Tools API
export const toolsAPI = {
  list: async () => {
    const response = await apiClient.get('/api/tools/list');
    return response.data;
  },

  get: async (toolName: string) => {
    const response = await apiClient.get(`/api/tools/${toolName}`);
    return response.data;
  },
};

// Evaluations API
export const evalsAPI = {
  run: async (evalName: string, agentType: string, testCases: any[]) => {
    const response = await apiClient.post('/api/evals/run', {
      eval_name: evalName,
      agent_type: agentType,
      test_cases: testCases,
    });
    return response.data;
  },

  getHistory: async (limit: number = 10, evalName?: string) => {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (evalName) params.append('eval_name', evalName);
    const response = await apiClient.get(`/api/evals/history?${params}`);
    return response.data;
  },
};

// Metrics API
export const metricsAPI = {
  getOverview: async () => {
    const response = await apiClient.get('/api/metrics/overview');
    return response.data;
  },

  getAgentStats: async () => {
    const response = await apiClient.get('/api/metrics/agent-stats');
    return response.data;
  },
};
