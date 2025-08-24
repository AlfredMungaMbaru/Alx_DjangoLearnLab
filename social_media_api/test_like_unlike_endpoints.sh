#!/bin/bash

# Test script for likes and unlike endpoints using cURL
echo "=== Testing Like and Unlike Endpoints ==="

BASE_URL="http://127.0.0.1:8000/api"

echo "1. Register/Login test user..."
# Register a test user
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/accounts/register/" \
    -H "Content-Type: application/json" \
    -d '{
        "username": "testliker",
        "email": "testliker@example.com", 
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Liker"
    }')

# Extract token from response
TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "Registration failed, trying login..."
    LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/accounts/login/" \
        -H "Content-Type: application/json" \
        -d '{
            "username": "testliker",
            "password": "testpass123"
        }')
    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
fi

echo "Token: $TOKEN"

echo ""
echo "2. Create a test post..."
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/posts/" \
    -H "Content-Type: application/json" \
    -H "Authorization: Token $TOKEN" \
    -d '{
        "title": "Test Post for Likes",
        "content": "This is a test post to test like/unlike endpoints."
    }')

POST_ID=$(echo $POST_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)
echo "Created post with ID: $POST_ID"

echo ""
echo "3. Like the post using /posts/$POST_ID/like/ endpoint..."
LIKE_RESPONSE=$(curl -s -X POST "$BASE_URL/posts/$POST_ID/like/" \
    -H "Authorization: Token $TOKEN")
echo "Like response: $LIKE_RESPONSE"

echo ""
echo "4. Check post details (should show 1 like)..."
POST_DETAILS=$(curl -s -X GET "$BASE_URL/posts/$POST_ID/" \
    -H "Authorization: Token $TOKEN")
echo "Post details: $POST_DETAILS"

echo ""
echo "5. Unlike the post using /posts/$POST_ID/unlike/ endpoint..."
UNLIKE_RESPONSE=$(curl -s -X POST "$BASE_URL/posts/$POST_ID/unlike/" \
    -H "Authorization: Token $TOKEN")
echo "Unlike response: $UNLIKE_RESPONSE"

echo ""
echo "6. Check post details again (should show 0 likes)..."
POST_DETAILS_AFTER=$(curl -s -X GET "$BASE_URL/posts/$POST_ID/" \
    -H "Authorization: Token $TOKEN")
echo "Post details after unlike: $POST_DETAILS_AFTER"

echo ""
echo "=== Test Complete ==="
