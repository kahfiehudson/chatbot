# Chatbot Starter — FastAPI + Ollama

## 1) Prereqs
- Docker & Docker Compose installed.
- A machine with CPU (works) or GPU (faster). NVIDIA GPUs need proper drivers + nvidia-container-runtime.

## 2) Clone & launch
```bash
git clone <this-project> chatbot
cd chatbot
# Pull images & start services
docker compose up -d --build

# Pull a model (in a separate terminal)
docker exec -it ollama ollama pull mistral:7b
# (alternatives: gemma2:2b, llama3.1:8b, qwen2:7b, etc.)
