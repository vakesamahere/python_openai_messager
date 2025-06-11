# LLM API Client

A Python client for interacting with Large Language Model APIs like OpenAI-compatible endpoints.

## Setup

1. Install the required modules:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on the provided `.env.sample` template and enter your API credentials:
```
LLM_URL_BASE = "your_api_base_url"
LLM_MODEL_NAME = "your_model_name"
LLM_API_KEY = "your_api_key"
```

## Features

- Send prompts to LLM APIs
- Stream responses with a typewriter effect
- Configurable model parameters (temperature, top_p, top_k, etc.)
- Comprehensive error handling

## Usage

Basic usage example:

```python
from llm import send_llm_chat_request, Typewriter

# Simple non-streaming request
response = send_llm_chat_request(
    prompt="What is artificial intelligence?",
    temperature=0.7,
    max_tokens=1024,
    stream=False
)
print(response)

# Streaming request with typewriter effect
response = send_llm_chat_request(
    prompt="Tell me a short story",
    temperature=0.9,
    max_tokens=2048,
    stream=True,
    typewriter=Typewriter(delay=0.02)
)
print("\nComplete response:")
print(response)
```

## Configuration

The following environment variables are required:
- `LLM_URL_BASE`: The base URL of the LLM API
- `LLM_MODEL_NAME`: The model name to use for requests
- `LLM_API_KEY`: Your API key for authentication
