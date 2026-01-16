#!/usr/bin/env python3
"""
Test script to verify the API is working properly and returning JSON responses
"""

import json
import requests
import sys

def test_api_responses():
    """Test that API endpoints return proper JSON responses"""

    base_url = "http://localhost:8000"  # Default FastAPI port

    print("Testing API endpoints for proper JSON responses...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint: Status {response.status_code}")

        # Check if response is JSON
        try:
            data = response.json()
            print(f"Health endpoint returned JSON: {data}")
        except json.JSONDecodeError:
            print(f"ERROR: Health endpoint returned non-JSON: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"Could not reach health endpoint: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
        return False

    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: Status {response.status_code}")

        # Check if response is JSON
        try:
            data = response.json()
            print(f"Root endpoint returned JSON: {data}")
        except json.JSONDecodeError:
            print(f"ERROR: Root endpoint returned non-JSON: {response.text[:200]}...")
            return False

    except Exception as e:
        print(f"Could not reach root endpoint: {e}")
        return False

    print("All endpoints returned proper JSON responses!")
    return True

if __name__ == "__main__":
    success = test_api_responses()
    if not success:
        sys.exit(1)
    print("\n✅ API JSON response test passed!")