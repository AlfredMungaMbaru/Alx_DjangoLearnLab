#!/usr/bin/env python3
"""
Test script for Social Media API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_user_registration():
    """Test user registration endpoint"""
    print("Testing user registration...")
    
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "bio": "Test user for API testing"
    }
    
    response = requests.post(f"{BASE_URL}/api/accounts/register/", json=data)
    
    if response.status_code == 201:
        print("✅ User registration successful!")
        result = response.json()
        print(f"User: {result['user']['username']}")
        print(f"Token: {result['token'][:20]}...")
        return result['token']
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(response.text)
        return None

def test_user_login():
    """Test user login endpoint"""
    print("\nTesting user login...")
    
    data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/accounts/login/", json=data)
    
    if response.status_code == 200:
        print("✅ User login successful!")
        result = response.json()
        print(f"User: {result['user']['username']}")
        print(f"Token: {result['token'][:20]}...")
        return result['token']
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_user_profile(token):
    """Test user profile endpoint"""
    print("\nTesting user profile...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/accounts/profile/", headers=headers)
    
    if response.status_code == 200:
        print("✅ Profile retrieval successful!")
        result = response.json()
        print(f"Profile: {json.dumps(result, indent=2)}")
        return True
    else:
        print(f"❌ Profile retrieval failed: {response.status_code}")
        print(response.text)
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Social Media API Tests\n")
    
    # Test registration
    token = test_user_registration()
    
    if token:
        # Test login
        login_token = test_user_login()
        
        if login_token:
            # Test profile with login token
            test_user_profile(login_token)
    
    print("\n🏁 Tests completed!")

if __name__ == "__main__":
    main()
