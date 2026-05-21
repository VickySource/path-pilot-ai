#!/usr/bin/env bash
set -euo pipefail
MODEL="${1:-llama3.1:8b}"
echo "Pulling Ollama model: $MODEL"
ollama pull "$MODEL"
