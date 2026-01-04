# DeepSeek Coder V2 Sidecar Service

This document provides connection details for integrating the DeepSeek Coder V2 model with IDEs and development tools.

## Service Configuration

**Provider**: OpenAI Compatible  
**Base URL**: `http://localhost:11434/v1`  
**Model ID**: `deepseek-coder-v2:16b`  
**API Key**: `ollama` (placeholder - no authentication required for local instance)

## Integration Details

The DeepSeek Coder V2 model is deployed in the `agy_ollama` container and accessible via the OpenAI-compatible API endpoint. This allows seamless integration with development tools that support OpenAI-style APIs.

### Example Request

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-coder-v2:16b",
    "messages": [
      {
        "role": "user",
        "content": "Write a Python function to calculate fibonacci sequence"
      }
    ]
  }'
```

### VS Code Integration

To use with VS Code extensions that support OpenAI-compatible APIs:

1. Set the API Base URL to: `http://localhost:11434/v1`
2. Set the Model to: `deepseek-coder-v2:16b`
3. Use `ollama` as the API key (or leave empty if the extension doesn't require it)

## Performance Notes

⚠️ **Model Swapping Latency**: When switching between different models (e.g., from Gemma2 to DeepSeek Coder), there may be a 2-3 second delay as the system loads the requested model into GPU memory. This is normal behavior for the Ollama container management.

## Hardware Specifications

**Target GPU**: GPU 0 (Titan RTX, 24GB VRAM)  
**Model Size**: ~16B parameters (8.9 GB VRAM usage)  
**Container**: `agy_ollama` on port 11434

## Testing

A test script is available at `tests/test_deepseek_sidecar.py` which validates the model endpoint connectivity and basic functionality.
