#!/usr/bin/env python3
"""
Test script for Flask Authentication API
Run this script to test all endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Flask Authentication API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Server is running")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Server is not responding")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://localhost:5000")
        return
    
    print("\n📝 Testing Registration")
    print("-" * 30)
    
    # Test 2: Register a new user
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        token = response.json().get('access_token')
        print("✅ Registration successful")
    else:
        print("❌ Registration failed")
        return
    
    print("\n🔑 Testing Login")
    print("-" * 30)
    
    # Test 3: Login with the registered user
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✅ Login successful")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print("❌ Login failed")
        return
    
    print("\n👤 Testing Current User Endpoint")
    print("-" * 30)
    
    # Test 4: Get current user info
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Current user endpoint working")
    else:
        print("❌ Current user endpoint failed")
    
    print("\n🛡️ Testing Protected Routes")
    print("-" * 30)
    
    # Test 5: Dashboard (protected)
    response = requests.get(f"{BASE_URL}/api/dashboard", headers=headers)
    print(f"Dashboard - Status: {response.status_code}")
    print(f"Dashboard - Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 6: Profile (protected)
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    print(f"Profile - Status: {response.status_code}")
    print(f"Profile - Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 7: Admin (should fail for non-admin)
    response = requests.get(f"{BASE_URL}/api/admin", headers=headers)
    print(f"Admin - Status: {response.status_code}")
    print(f"Admin - Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n🔒 Testing Invalid Token")
    print("-" * 30)
    
    # Test 8: Try to access protected route without token
    response = requests.get(f"{BASE_URL}/api/dashboard")
    print(f"No Token - Status: {response.status_code}")
    print(f"No Token - Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 9: Try to access protected route with invalid token
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/api/dashboard", headers=invalid_headers)
    print(f"Invalid Token - Status: {response.status_code}")
    print(f"Invalid Token - Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n🎯 Testing Admin User")
    print("-" * 30)
    
    # Create admin user and test admin access
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=admin_data)
    if response.status_code == 201:
        admin_token = response.json().get('access_token')
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = requests.get(f"{BASE_URL}/api/admin", headers=admin_headers)
        print(f"Admin Access - Status: {response.status_code}")
        print(f"Admin Access - Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n✅ Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
