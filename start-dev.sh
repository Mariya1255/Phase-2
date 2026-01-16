#!/bin/bash
# Startup script for the Todo application

echo "Starting Todo Application..."

# Start the backend server
echo "Starting backend server..."
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload &
BACKEND_PID=$!

# Give the backend a moment to start
sleep 3

# Start the frontend server
echo "Starting frontend server..."
cd ../frontend
npm install
npm run dev &

# Wait for both processes
wait $BACKEND_PID