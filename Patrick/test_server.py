#!/usr/bin/env python3
"""
Test script for the EinsteinDB server.
"""
import requests
import json
import time

def test_server():
    base_url = "http://localhost:8000"
    
    # Test GET /status
    print("Testing GET /status...")
    try:
        response = requests.get(f"{base_url}/status")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test POST /query
    print("\nTesting POST /query...")
    try:
        data = {
            "query": "SELECT * FROM test_table LIMIT 10",
            "database": "test_db"
        }
        response = requests.post(
            f"{base_url}/query",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Waiting for server to start...")
    time.sleep(2)  # Give the server time to start
    test_server()
