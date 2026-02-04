# API Usage Examples

This document provides practical examples of using the AI Agent Toolbox API.

## Table of Contents

1. [Authentication](#authentication)
2. [Agents](#agents)
3. [Tools](#tools)
4. [Evaluations](#evaluations)
5. [Metrics](#metrics)

## Authentication

Currently, the API does not require authentication. This is suitable for local development but should be secured in production.

## Agents

### Run a Research Agent

**Python:**
```python
import requests

url = "http://localhost:8000/api/agents/run"
payload = {
    "query": "What is machine learning and how does it work?",
    "agent_type": "research",
    "stream": False
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Response: {result['response']}")
print(f"Duration: {result['duration_ms']}ms")
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/api/agents/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What is machine learning and how does it work?',
    agent_type: 'research',
    stream: false
  })
});

const result = await response.json();
console.log('Response:', result.response);
```

**cURL:**
```bash
curl -X POST http://localhost:8000/api/agents/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "agent_type": "research",
    "stream": false
  }'
```

### Run a Code Agent

```python
import requests

url = "http://localhost:8000/api/agents/run"
payload = {
    "query": "Write a Python function to calculate fibonacci numbers",
    "agent_type": "code",
    "stream": False
}

response = requests.post(url, json=payload)
print(response.json()['response'])
```

### Stream Agent Responses (SSE)

**Python with SSE:**
```python
import requests
import json

url = "http://localhost:8000/api/agents/stream"
payload = {
    "query": "Explain quantum computing",
    "agent_type": "research"
}

with requests.post(url, json=payload, stream=True) as response:
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = line[6:]  # Remove 'data: ' prefix
                if data == '[DONE]':
                    break
                try:
                    chunk = json.loads(data)
                    print(chunk)
                except json.JSONDecodeError:
                    pass
```

**JavaScript with EventSource:**
```javascript
const eventSource = new EventSource(
  'http://localhost:8000/api/agents/stream?query=Explain%20quantum%20computing&agent_type=research'
);

eventSource.onmessage = (event) => {
  if (event.data === '[DONE]') {
    eventSource.close();
    return;
  }
  
  const chunk = JSON.parse(event.data);
  console.log('Chunk:', chunk);
};

eventSource.onerror = (error) => {
  console.error('Error:', error);
  eventSource.close();
};
```

### Get Agent History

```python
import requests

# Get last 10 runs
response = requests.get('http://localhost:8000/api/agents/history?limit=10')
history = response.json()

for run in history:
    print(f"ID: {run['id']}, Type: {run['agent_type']}, Status: {run['status']}")
```

## Tools

### List All Available Tools

```python
import requests

response = requests.get('http://localhost:8000/api/tools/list')
tools = response.json()

for tool in tools:
    print(f"Tool: {tool['name']}")
    print(f"Description: {tool['description']}")
    print(f"Agent Types: {', '.join(tool['agent_types'])}")
    print()
```

### Get Specific Tool Details

```python
import requests

response = requests.get('http://localhost:8000/api/tools/calculator')
tool = response.json()
print(tool)
```

## Evaluations

### Run a Simple Evaluation

```python
import requests

url = "http://localhost:8000/api/evals/run"
payload = {
    "eval_name": "math_test",
    "agent_type": "research",
    "test_cases": [
        {
            "test_case": "What is 2 + 2?",
            "expected": "4"
        },
        {
            "test_case": "What is 10 * 5?",
            "expected": "50"
        },
        {
            "test_case": "What is 100 / 4?",
            "expected": "25"
        }
    ]
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Evaluation: {result['eval_name']}")
print(f"Total Tests: {result['total_tests']}")
print(f"Passed: {result['passed']}")
print(f"Failed: {result['failed']}")
print(f"Average Score: {result['average_score']:.2%}")

for test_result in result['results']:
    status = "✓" if test_result['passed'] else "✗"
    print(f"{status} {test_result['test_case']}: {test_result['score']:.2%}")
```

### Run a Code Quality Evaluation

```python
import requests

url = "http://localhost:8000/api/evals/run"
payload = {
    "eval_name": "code_quality",
    "agent_type": "code",
    "test_cases": [
        {
            "test_case": "Write a function to reverse a string in Python",
            "expected": "def"  # Check if it contains a function definition
        },
        {
            "test_case": "Create a class for a simple bank account",
            "expected": "class"  # Check if it contains a class
        }
    ]
}

response = requests.post(url, json=payload)
print(response.json())
```

### Get Evaluation History

```python
import requests

# Get all evaluations
response = requests.get('http://localhost:8000/api/evals/history?limit=20')
evals = response.json()

# Get evaluations for a specific test
response = requests.get('http://localhost:8000/api/evals/history?eval_name=math_test&limit=10')
math_evals = response.json()

for eval in math_evals:
    status = "✓ PASSED" if eval['passed'] else "✗ FAILED"
    print(f"{status} - Score: {eval['score']:.2%} - {eval['created_at']}")
```

## Metrics

### Get System Overview

```python
import requests

response = requests.get('http://localhost:8000/api/metrics/overview')
metrics = response.json()

print(f"Total Runs: {metrics['total_runs']}")
print(f"Average Duration: {metrics['average_duration_ms']:.2f}ms")
print(f"Total Tool Calls: {metrics['total_tool_calls']}")
print(f"Total Evaluations: {metrics['total_evaluations']}")
print(f"Average Eval Score: {metrics['average_eval_score']:.2%}")
```

### Get Agent Statistics

```python
import requests

response = requests.get('http://localhost:8000/api/metrics/agent-stats')
stats = response.json()

for agent_stat in stats:
    print(f"Agent Type: {agent_stat['agent_type']}")
    print(f"  Total Runs: {agent_stat['total_runs']}")
    print(f"  Avg Duration: {agent_stat['average_duration_ms']:.2f}ms")
    print()
```

## Complete Workflow Example

Here's a complete example that demonstrates a full workflow:

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. Run an agent
print("1. Running agent...")
agent_response = requests.post(
    f"{BASE_URL}/api/agents/run",
    json={
        "query": "What is the capital of France?",
        "agent_type": "research"
    }
)
run_result = agent_response.json()
print(f"Response: {run_result['response']}")

# 2. List available tools
print("\n2. Listing tools...")
tools_response = requests.get(f"{BASE_URL}/api/tools/list")
tools = tools_response.json()
print(f"Available tools: {', '.join([t['name'] for t in tools])}")

# 3. Run evaluation
print("\n3. Running evaluation...")
eval_response = requests.post(
    f"{BASE_URL}/api/evals/run",
    json={
        "eval_name": "geography_test",
        "agent_type": "research",
        "test_cases": [
            {"test_case": "What is the capital of France?", "expected": "Paris"},
            {"test_case": "What is the capital of Japan?", "expected": "Tokyo"}
        ]
    }
)
eval_result = eval_response.json()
print(f"Evaluation score: {eval_result['average_score']:.2%}")

# 4. Get metrics
print("\n4. Getting metrics...")
metrics_response = requests.get(f"{BASE_URL}/api/metrics/overview")
metrics = metrics_response.json()
print(f"System metrics: {metrics}")

print("\n✓ Workflow completed successfully!")
```

## Error Handling

Always handle potential errors:

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/agents/run",
        json={"query": "test", "agent_type": "research"},
        timeout=30
    )
    response.raise_for_status()  # Raises HTTPError for bad status codes
    result = response.json()
    print(result)
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

## Rate Limiting and Best Practices

- Be mindful of OpenAI API rate limits
- Cache responses when possible using Redis
- Use streaming for long-running queries
- Implement proper error handling
- Monitor metrics to track performance
