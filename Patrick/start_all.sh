#!/bin/bash

# Start the EinsteinDB server
echo "Starting EinsteinDB Server..."
cd "$(dirname "$0")/src-EinsteinDBGPT3/EinsteinDB-GPT3-server"
python einsteindb_server.py --port 8000 --debug &
EINSTEINDB_PID=$!
echo "EinsteinDB Server started with PID: $EINSTEINDB_PID"

# Start the QNoether component
echo -e "\nStarting QNoether component..."
cd "../src-QNoether"
python run_job.py &
QNOETHER_PID=$!
echo "QNoether component started with PID: $QNOETHER_PID"

# Function to handle script termination
cleanup() {
    echo -e "\nShutting down components..."
    kill $EINSTEINDB_PID $QNOETHER_PID 2>/dev/null
    wait $EINSTEINDB_PID $QNOETHER_PID 2>/dev/null
    echo "All components have been stopped."
    exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

echo -e "\nPatrick components are now running. Press Ctrl+C to stop all components."

# Keep the script running
while true; do
    sleep 1
done
