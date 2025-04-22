FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y wget python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY start_llm.sh .

RUN chmod +x start_llm.sh
CMD ["./start_llm.sh"]