#!/bin/sh

communication_type="${ORDER_COMMUNICATION_TYPE}"

if [ "$communication_type" = "http" ]; then
    uv run fastapi run ./src/main.py --proxy-headers --port 80
    
elif [ "$communication_type" = "broker" ]; then
    uv run faststream run src.main:app

elif [ "$communication_type" = "grpc" ]; then
    uv run python -m src.main

else
    echo "communication_type has not been set"
    exit 1

fi