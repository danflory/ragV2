# Local Model Setup for Cline Integration

This guide explains how to set up and use local models with Cline via the OpenAI-compatible API endpoint at `http://localhost:11434/v1`.

## Overview

The AntiGravity RAG system provides local model inference through Ollama containers running on a dual-GPU setup. Cline can directly integrate with these local models using the standard OpenAI API format.

## System Architecture

### GPU 0: Generation (Titan RTX 24GB)
- **Container**: `agy_ollama`
- **Port**: `11434`
- **API Endpoint**: `http://localhost:11434/v1`
- **Models**: 
  - `deepseek-coder-v2:16b` (~8.9GB VRAM)
  - `codellama:7b` (~3.8GB VRAM)

### GPU 1: Embeddings (GTX 1060 6GB)
- **Container**: `agy_ollama_embed`
- **Port**: `11435`
- **API Endpoint**: `http://localhost:11435/v1`

## Setting Up Local Models for Cline

### 1. Verify Container Health

First, ensure the Ollama container is running:

```bash
docker ps | grep agy_ollama
```

Expected output:
```
CONTAINER ID   IMAGE                COMMAND                  CREATED       STATUS       PORTS                      NAMES
xxxxxxxxxxxx   ollama/ollama:latest "ollama serve"          2 hours ago   Up 2 hours   0.0.0.0:11434->11434/tcp   agy_ollama
```

### 2. Check Available Models

List currently installed models:

```bash
curl http://localhost:11434/api/tags
```

### 3. Install New Models (if needed)

To add a new model to the local system:

```bash
docker exec agy_ollama ollama pull <model-name>
```

Example:
```bash
docker exec agy_ollama ollama pull deepseek-coder-v2:16b
```

## Cline Integration Configuration

### API Endpoint Configuration

Cline can use the local models by configuring the OpenAI-compatible endpoint:

- **Base URL**: `http://localhost:11434/v1`
- **API Key**: `ollama` (placeholder - no authentication required for local instances)

### Model Selection

Available models for development:
- **Coding**: `deepseek-coder-v2:16b` - 16B parameter coding model
- **General**: `codellama:7b` - 7B parameter general purpose model

### Example Cline Configuration

When configuring Cline to use local models, set these parameters:

```python
# For DeepSeek Coder (recommended for development)
model_config = {
    "provider": "openai",
    "base_url": "http://localhost:11434/v1",
    "model": "deepseek-coder-v2:16b",
    "api_key": "ollama"
}

# For CodeLlama (lightweight alternative)
model_config = {
    "provider": "openai", 
    "base_url": "http://localhost:11434/v1",
    "model": "codellama:7b",
    "api_key": "ollama"
}
```

## Testing the Connection

### Using curl

Test the model endpoint with a simple request:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-coder-v2:16b",
    "messages": [
      {
        "role": "user",
        "content": "Print hello world in python"
      }
    ]
  }'
```

### Using Python

```python
import requests

def test_local_model():
    url = "http://localhost:11434/v1/chat/completions"
    
    payload = {
        "model": "deepseek-coder-v2:16b",
        "messages": [
            {
                "role": "user", 
                "content": "Print hello world in python"
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(result['choices'][0]['message']['content'])
    else:
        print(f"Error: {response.status_code}")

test_local_model()
```

## Performance Considerations

### Model Swapping Latency

⚠️ **Important**: When switching between different models (e.g., from CodeLlama to DeepSeek Coder), there may be a 2-3 second delay as the system loads the requested model into GPU memory. This is normal behavior for the Ollama container management.

### VRAM Management

- **Titan RTX (24GB)**: Can comfortably run one large model at a time
- **Current Usage**: DeepSeek Coder (~8.9GB) + CodeLlama (~3.8GB) = ~12.7GB
- **Available**: ~11GB headroom for extended conversations

### Hardware Specifications

| Component | Specification |
|-----------|---------------|
| **GPU 0** | NVIDIA Titan RTX (24GB VRAM) |
| **GPU 1** | NVIDIA GTX 1060 (6GB VRAM) |
| **Container** | `agy_ollama` on port 11434 |
| **Model Size Limit** | ~16B parameters for Titan RTX |

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure Docker containers are running
   ```bash
   docker-compose up -d
   ```

2. **Model Not Found**: Pull the required model
   ```bash
   docker exec agy_ollama ollama pull deepseek-coder-v2:16b
   ```

3. **VRAM Issues**: Monitor GPU usage
   ```bash
   nvidia-smi
   ```

### Verification Script

A test script is available to verify the setup:

```bash
python tests/test_deepseek_sidecar.py
```

## Integration with Development Tools

### VS Code Integration

To use with VS Code extensions that support OpenAI-compatible APIs:

1. Set the API Base URL to: `http://localhost:11434/v1`
2. Set the Model to: `deepseek-coder-v2:16b`
3. Use `ollama` as the API key (or leave empty if the extension doesn't require it)

### Cline Act Mode Usage

When Cline is in Act mode, it can directly call the local model endpoint:

```python
# Cline can make direct API calls
response = requests.post(
    "http://localhost:11434/v1/chat/completions",
    json={
        "model": "deepseek-coder-v2:16b",
        "messages": [{"role": "user", "content": prompt}]
    }
)
```

This enables Cline to perform local inference without network latency or external API costs while maintaining full OpenAI API compatibility.
