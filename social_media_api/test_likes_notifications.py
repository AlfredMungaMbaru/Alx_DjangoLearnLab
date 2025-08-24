#!/usr/bin/env python3
"""
Test script for likes and notifications functionality in the Social Media API
"""

import requests
import json

# API Base URL
BASE_URL = "http://127.0.0.1:8000/api"

def test_likes_and_notifications():
    """Test the likes and notifications functionality"""
    
    print("=== Testing Likes and Notifications Functionality ===\n")
    
    # Test data
    user1_data = {
        "username": "alice_likes",
        "email": "alice.likes@example.com",
        "password": "testpass123",
        "first_name": "Alice",
        "last_name": "Johnson"
    }
    
    user2_data = {
        "username": "bob_likes",
        "email": "bob.likes@example.com",
        "password": "testpass123",
        "first_name": "Bob",
        "last_name": "Smith"
    }
    
    # Register users
    print("1. Registering test users...")
    user1_response = requests.post(f"{BASE_URL}/accounts/register/", json=user1_data)
    user2_response = requests.post(f"{BASE_URL}/accounts/register/", json=user2_data)
    
    if user1_response.status_code == 201:
        user1_token = user1_response.json()['token']
        print(f"✓ User1 registered: {user1_data['username']}")
    else:
        # Try to login if user already exists
        login_response = requests.post(f"{BASE_URL}/accounts/login/", json={
            "username": user1_data['username'],
            "password": user1_data['password']
        })
        if login_response.status_code == 200:
            user1_token = login_response.json()['token']
            print(f"✓ User1 logged in: {user1_data['username']}")
        else:
            print(f"✗ Failed to register/login user1: {user1_response.text}")
            return
    
    if user2_response.status_code == 201:
        user2_token = user2_response.json()['token']
        print(f"✓ User2 registered: {user2_data['username']}")
    else:
        # Try to login if user already exists
        login_response = requests.post(f"{BASE_URL}/accounts/login/", json={
            "username": user2_data['username'],
            "password": user2_data['password']
        })
        if login_response.status_code == 200:
            user2_token = login_response.json()['token']
            print(f"✓ User2 logged in: {user2_data['username']}")
        else:
            print(f"✗ Failed to register/login user2: {user2_response.text}")
            return
    
    # Headers for authenticated requests
    user1_headers = {"Authorization": f"Token {user1_token}"}
    user2_headers = {"Authorization": f"Token {user2_token}"}
    
    print()
    
    # Create a post by user1
    print("2. Creating a post by user1...")
    post_data = {
        "title": "Test Post for Likes",
        "content": "This is a test post to test the likes functionality."
    }
    
    post_response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=user1_headers)
    if post_response.status_code == 201:
        post_id = post_response.json()['id']
        print(f"✓ Post created with ID: {post_id}")
    else:
        print(f"✗ Failed to create post: {post_response.text}")
        return
    
    print()
    
    # User2 follows user1 (should create notification)
    print("3. User2 follows user1...")
    follow_response = requests.post(f"{BASE_URL}/accounts/follow/{user1_response.json().get('user', {}).get('id', 1)}/", headers=user2_headers)
    if follow_response.status_code == 200:
        print("✓ User2 is now following user1")
    else:
        print(f"✗ Failed to follow: {follow_response.text}")
    
    print()
    
    # User2 likes the post (should create notification)
    print("4. User2 likes the post...")
    like_response = requests.post(f"{BASE_URL}/posts/{post_id}/like/", headers=user2_headers)
    if like_response.status_code == 201:
        print(f"✓ Post liked: {like_response.json()}")
    else:
        print(f"✗ Failed to like post: {like_response.text}")
    
    print()
    
    # Check the post details (should show likes count and is_liked_by_user)
    print("5. Checking post details with likes info...")
    post_detail_response = requests.get(f"{BASE_URL}/posts/{post_id}/", headers=user2_headers)
    if post_detail_response.status_code == 200:
        post_data = post_detail_response.json()
        print(f"✓ Post details:")
        print(f"  - Likes count: {post_data.get('likes_count', 0)}")
        print(f"  - Is liked by user2: {post_data.get('is_liked_by_user', False)}")
    else:
        print(f"✗ Failed to get post details: {post_detail_response.text}")
    
    print()
    
    # User2 comments on the post (should create notification)
    print("6. User2 comments on the post...")
    comment_data = {
        "content": "Great post! I really liked it.",
        "post": post_id
    }
    comment_response = requests.post(f"{BASE_URL}/comments/", json=comment_data, headers=user2_headers)
    if comment_response.status_code == 201:
        print(f"✓ Comment created: {comment_response.json()['id']}")
    else:
        print(f"✗ Failed to create comment: {comment_response.text}")
    
    print()
    
    # Check user1's notifications
    print("7. Checking user1's notifications...")
    notifications_response = requests.get(f"{BASE_URL}/notifications/", headers=user1_headers)
    if notifications_response.status_code == 200:
        notifications_data = notifications_response.json()
        print(f"✓ User1 has {notifications_data.get('unread_count', 0)} unread notifications")
        
        notifications = notifications_data.get('notifications', [])
        for i, notification in enumerate(notifications, 1):
            print(f"  {i}. {notification['actor']['username']} {notification['verb']} ({notification['timestamp']})")
    else:
        print(f"✗ Failed to get notifications: {notifications_response.text}")
    
    print()
    
    # User2 unlikes the post
    print("8. User2 unlikes the post...")
    unlike_response = requests.delete(f"{BASE_URL}/posts/{post_id}/like/", headers=user2_headers)
    if unlike_response.status_code == 200:
        print(f"✓ Post unliked: {unlike_response.json()}")
    else:
        print(f"✗ Failed to unlike post: {unlike_response.text}")
    
    print()
    
    # Check post details again (should show 0 likes)
    print("9. Checking post details after unlike...")
    post_detail_response = requests.get(f"{BASE_URL}/posts/{post_id}/", headers=user2_headers)
    if post_detail_response.status_code == 200:
        post_data = post_detail_response.json()
        print(f"✓ Post details after unlike:")
        print(f"  - Likes count: {post_data.get('likes_count', 0)}")
        print(f"  - Is liked by user2: {post_data.get('is_liked_by_user', False)}")
    else:
        print(f"✗ Failed to get post details: {post_detail_response.text}")
    
    print()
    
    # Mark first notification as read
    print("10. Marking first notification as read...")
    notifications_response = requests.get(f"{BASE_URL}/notifications/", headers=user1_headers)
    if notifications_response.status_code == 200:
        notifications = notifications_response.json().get('notifications', [])
        if notifications:
            first_notification_id = notifications[0]['id']
            mark_read_response = requests.patch(f"{BASE_URL}/notifications/{first_notification_id}/mark-read/", headers=user1_headers)
            if mark_read_response.status_code == 200:
                print(f"✓ Notification {first_notification_id} marked as read")
            else:
                print(f"✗ Failed to mark notification as read: {mark_read_response.text}")
        else:
            print("No notifications to mark as read")
    
    print()
    
    # Mark all notifications as read
    print("11. Marking all notifications as read...")
    mark_all_read_response = requests.patch(f"{BASE_URL}/notifications/mark-all-read/", headers=user1_headers)
    if mark_all_read_response.status_code == 200:
        print(f"✓ All notifications marked as read: {mark_all_read_response.json()}")
    else:
        print(f"✗ Failed to mark all notifications as read: {mark_all_read_response.text}")
    
    print()
    
    # Check notifications again (should show 0 unread)
    print("12. Checking notifications after marking all as read...")
    notifications_response = requests.get(f"{BASE_URL}/notifications/", headers=user1_headers)
    if notifications_response.status_code == 200:
        notifications_data = notifications_response.json()
        print(f"✓ User1 now has {notifications_data.get('unread_count', 0)} unread notifications")
    else:
        print(f"✗ Failed to get notifications: {notifications_response.text}")
    
    print("\n=== Likes and Notifications Testing Complete ===")

if __name__ == "__main__":
    test_likes_and_notifications()
