#!/usr/bin/env python3
"""
Test script for Follow and Feed functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def create_test_user(username, email, password):
    """Create a test user and return their token"""
    print(f"🔐 Creating user: {username}")
    
    # Try to register
    register_data = {
        "username": username,
        "email": email,
        "password": password,
        "password_confirm": password,
        "bio": f"Test user {username}"
    }
    
    response = requests.post(f"{BASE_URL}/api/accounts/register/", json=register_data)
    
    if response.status_code == 201:
        result = response.json()
        token = result['token']
        user_id = result['user']['id']
        print(f"✅ User {username} registered successfully (ID: {user_id})")
        return token, user_id
    else:
        # Try to login if user already exists
        login_data = {"username": username, "password": password}
        response = requests.post(f"{BASE_URL}/api/accounts/login/", json=login_data)
        
        if response.status_code == 200:
            result = response.json()
            token = result['token']
            user_id = result['user']['id']
            print(f"✅ User {username} logged in successfully (ID: {user_id})")
            return token, user_id
        else:
            print(f"❌ Failed to authenticate {username}: {response.text}")
            return None, None

def create_test_post(token, title, content):
    """Create a test post"""
    headers = {"Authorization": f"Token {token}"}
    post_data = {"title": title, "content": content}
    
    response = requests.post(f"{BASE_URL}/api/posts/", json=post_data, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Post created: '{result['title']}'")
        return result['id']
    else:
        print(f"❌ Post creation failed: {response.text}")
        return None

def test_follow_functionality():
    """Test the follow/unfollow functionality"""
    print("\n🚀 Testing Follow and Feed Functionality")
    print("=" * 50)
    
    # Create test users
    alice_token, alice_id = create_test_user("alice_follow", "alice@example.com", "testpass123")
    bob_token, bob_id = create_test_user("bob_follow", "bob@example.com", "testpass123")
    charlie_token, charlie_id = create_test_user("charlie_follow", "charlie@example.com", "testpass123")
    
    if not all([alice_token, bob_token, charlie_token]):
        print("❌ Failed to create test users")
        return
    
    print(f"\nTest users created:")
    print(f"  - Alice (ID: {alice_id})")
    print(f"  - Bob (ID: {bob_id})")
    print(f"  - Charlie (ID: {charlie_id})")
    
    # Test 1: Alice follows Bob
    print(f"\n📍 Test 1: Alice follows Bob")
    headers = {"Authorization": f"Token {alice_token}"}
    response = requests.post(f"{BASE_URL}/api/accounts/follow/{bob_id}/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
        print(f"   Bob now has {result['user']['followers_count']} followers")
    else:
        print(f"❌ Follow failed: {response.text}")
    
    # Test 2: Alice follows Charlie
    print(f"\n📍 Test 2: Alice follows Charlie")
    response = requests.post(f"{BASE_URL}/api/accounts/follow/{charlie_id}/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Follow failed: {response.text}")
    
    # Test 3: Check Alice's following list
    print(f"\n📍 Test 3: Check Alice's following list")
    response = requests.get(f"{BASE_URL}/api/accounts/following/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Alice is following {result['following_count']} users:")
        for user in result['following']:
            print(f"   - {user['username']} (ID: {user['id']})")
    else:
        print(f"❌ Failed to get following list: {response.text}")
    
    # Test 4: Bob creates some posts
    print(f"\n📍 Test 4: Bob creates posts")
    bob_headers = {"Authorization": f"Token {bob_token}"}
    post1_id = create_test_post(bob_token, "Bob's First Post", "Hello from Bob! This is my first post.")
    post2_id = create_test_post(bob_token, "Bob's Second Post", "Another great post from Bob!")
    
    # Test 5: Charlie creates a post
    print(f"\n📍 Test 5: Charlie creates a post")
    charlie_headers = {"Authorization": f"Token {charlie_token}"}
    post3_id = create_test_post(charlie_token, "Charlie's Adventure", "Charlie here! Just had an amazing adventure.")
    
    # Test 6: Alice checks her feed
    print(f"\n📍 Test 6: Alice checks her feed")
    response = requests.get(f"{BASE_URL}/api/feed/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Alice's feed loaded successfully")
        print(f"   Following {result['following_count']} users")
        
        if 'results' in result:
            posts = result['results']['posts']
        else:
            posts = result['posts']
            
        print(f"   Feed contains {len(posts)} posts:")
        for post in posts:
            print(f"   - '{post['title']}' by {post['author']['username']}")
    else:
        print(f"❌ Failed to load feed: {response.text}")
    
    # Test 7: Test unfollow
    print(f"\n📍 Test 7: Alice unfollows Bob")
    response = requests.post(f"{BASE_URL}/api/accounts/unfollow/{bob_id}/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['message']}")
    else:
        print(f"❌ Unfollow failed: {response.text}")
    
    # Test 8: Check feed after unfollow
    print(f"\n📍 Test 8: Alice checks feed after unfollowing Bob")
    response = requests.get(f"{BASE_URL}/api/feed/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        
        if 'results' in result:
            posts = result['results']['posts']
        else:
            posts = result['posts']
            
        print(f"✅ Feed now contains {len(posts)} posts:")
        for post in posts:
            print(f"   - '{post['title']}' by {post['author']['username']}")
    else:
        print(f"❌ Failed to load feed: {response.text}")
    
    # Test 9: Test edge cases
    print(f"\n📍 Test 9: Test edge cases")
    
    # Try to follow yourself
    response = requests.post(f"{BASE_URL}/api/accounts/follow/{alice_id}/", headers=headers)
    if response.status_code == 400:
        print("✅ Correctly prevented self-follow")
    else:
        print("❌ Should not allow self-follow")
    
    # Try to follow same user twice
    response = requests.post(f"{BASE_URL}/api/accounts/follow/{charlie_id}/", headers=headers)
    if response.status_code == 400:
        print("✅ Correctly prevented duplicate follow")
    else:
        print("❌ Should not allow duplicate follow")
    
    print(f"\n🏁 Follow and Feed tests completed!")

if __name__ == "__main__":
    test_follow_functionality()
