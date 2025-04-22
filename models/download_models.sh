#!/bin/bash

mkdir -p models/embeddings models/llm

# Download embedding model
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/pytorch_model.bin -P models/embeddings/

# Download quantized Mistral
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -P models/llm/