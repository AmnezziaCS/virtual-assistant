#!/bin/bash

# Download models
chmod +x models/download_models.sh
./models/download_models.sh

# Build and start containers
docker-compose build
docker-compose up -d

echo "System is running!"
echo "API available at http://localhost:8000"