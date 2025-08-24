#!/usr/bin/env python3
"""
Test script for Posts and Comments API endpoints
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_user_registration_and_login():
    """Create a test user and get authentication token"""
    print("🔐 Setting up test user...")
    
    # Register user
    register_data = {
        "username": "testuser_posts",
        "email": "testposts@example.com",
        "password": "testpass123",
        "password_confirm": "testpass123",
        "bio": "Test user for posts API"
    }
    
    response = requests.post(f"{BASE_URL}/api/accounts/register/", json=register_data)
    
    if response.status_code == 201:
        result = response.json()
        token = result['token']
        print(f"✅ User registered successfully: {result['user']['username']}")
        return token
    else:
        # Try to login if user already exists
        login_data = {
            "username": "testuser_posts",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/api/accounts/login/", json=login_data)
        if response.status_code == 200:
            result = response.json()
            token = result['token']
            print(f"✅ User logged in successfully: {result['user']['username']}")
            return token
        else:
            print(f"❌ Authentication failed: {response.text}")
            return None

def test_create_post(token):
    """Test creating a new post"""
    print("\n📝 Testing post creation...")
    
    headers = {"Authorization": f"Token {token}"}
    post_data = {
        "title": "My First Post",
        "content": "This is the content of my first post. It's about testing the API!"
    }
    
    response = requests.post(f"{BASE_URL}/api/posts/", json=post_data, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Post created successfully: {result['title']}")
        print(f"Post ID: {result['id']}")
        return result['id']
    else:
        print(f"❌ Post creation failed: {response.status_code}")
        print(response.text)
        return None

def test_list_posts(token):
    """Test listing all posts"""
    print("\n📋 Testing posts listing...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/posts/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Posts listed successfully")
        print(f"Total posts: {result.get('count', 'N/A')}")
        if result.get('results'):
            for post in result['results'][:3]:  # Show first 3 posts
                print(f"  - {post['title']} by {post['author']['username']}")
        return True
    else:
        print(f"❌ Posts listing failed: {response.status_code}")
        return False

def test_get_post_detail(token, post_id):
    """Test getting post details"""
    print(f"\n🔍 Testing post detail retrieval (ID: {post_id})...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/posts/{post_id}/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Post details retrieved successfully")
        print(f"Title: {result['title']}")
        print(f"Comments count: {result['comments_count']}")
        return True
    else:
        print(f"❌ Post detail retrieval failed: {response.status_code}")
        return False

def test_create_comment(token, post_id):
    """Test creating a comment on a post"""
    print(f"\n💬 Testing comment creation for post {post_id}...")
    
    headers = {"Authorization": f"Token {token}"}
    comment_data = {
        "post": post_id,
        "content": "This is a test comment on the post!"
    }
    
    response = requests.post(f"{BASE_URL}/api/comments/", json=comment_data, headers=headers)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Comment created successfully")
        print(f"Comment ID: {result['id']}")
        return result['id']
    else:
        print(f"❌ Comment creation failed: {response.status_code}")
        print(response.text)
        return None

def test_list_comments(token):
    """Test listing all comments"""
    print("\n💬 Testing comments listing...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/comments/", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Comments listed successfully")
        print(f"Total comments: {result.get('count', 'N/A')}")
        return True
    else:
        print(f"❌ Comments listing failed: {response.status_code}")
        return False

def test_search_posts(token):
    """Test searching posts"""
    print("\n🔍 Testing post search...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/posts/?search=first", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Post search successful")
        print(f"Search results: {result.get('count', 0)} posts found")
        return True
    else:
        print(f"❌ Post search failed: {response.status_code}")
        return False

def test_pagination(token):
    """Test pagination"""
    print("\n📄 Testing pagination...")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/posts/?page=1&page_size=5", headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pagination test successful")
        print(f"Page size: {len(result.get('results', []))}")
        print(f"Next page: {'Yes' if result.get('next') else 'No'}")
        return True
    else:
        print(f"❌ Pagination test failed: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Posts and Comments API Tests\n")
    
    # Setup authentication
    token = test_user_registration_and_login()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test post operations
    post_id = test_create_post(token)
    test_list_posts(token)
    
    if post_id:
        test_get_post_detail(token, post_id)
        
        # Test comment operations
        comment_id = test_create_comment(token, post_id)
        test_list_comments(token)
    
    # Test search and pagination
    test_search_posts(token)
    test_pagination(token)
    
    print("\n🏁 All tests completed!")

if __name__ == "__main__":
    main()
