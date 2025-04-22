#!/bin/bash

# Download llama.cpp if not present
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp && make
fi

# Start the LLM server
./llama.cpp/server -m /models/mistral-7b-instruct-v0.1.Q4_K_M.gguf --port 8001