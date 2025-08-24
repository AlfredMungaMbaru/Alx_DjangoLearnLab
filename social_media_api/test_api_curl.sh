#!/bin/bash

# Simple bash script to test Posts and Comments API
BASE_URL="http://127.0.0.1:8000"

echo "🚀 Testing Posts and Comments API with curl"
echo "==========================================="

# Test 1: Register a user
echo ""
echo "📝 Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser_curl",
    "email": "testcurl@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Test user created via curl"
  }')

if echo "$REGISTER_RESPONSE" | grep -q "token"; then
    TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
    echo "✅ User registered successfully"
    echo "Token: ${TOKEN:0:20}..."
else
    echo "❌ Registration failed or user exists, trying login..."
    # Try login if registration fails
    LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/login/" \
      -H "Content-Type: application/json" \
      -d '{
        "username": "testuser_curl",
        "password": "testpass123"
      }')
    
    if echo "$LOGIN_RESPONSE" | grep -q "token"; then
        TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
        echo "✅ User logged in successfully"
        echo "Token: ${TOKEN:0:20}..."
    else
        echo "❌ Authentication failed"
        echo "$LOGIN_RESPONSE"
        exit 1
    fi
fi

# Test 2: Create a post
echo ""
echo "📝 Testing post creation..."
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/posts/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "title": "Test Post via curl",
    "content": "This is a test post created using curl to test the API functionality."
  }')

if echo "$POST_RESPONSE" | grep -q "id"; then
    POST_ID=$(echo "$POST_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    echo "✅ Post created successfully"
    echo "Post ID: $POST_ID"
else
    echo "❌ Post creation failed"
    echo "$POST_RESPONSE"
    exit 1
fi

# Test 3: List posts
echo ""
echo "📋 Testing posts listing..."
LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/api/posts/" \
  -H "Authorization: Token $TOKEN")

if echo "$LIST_RESPONSE" | grep -q "results"; then
    COUNT=$(echo "$LIST_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])")
    echo "✅ Posts listed successfully"
    echo "Total posts: $COUNT"
else
    echo "❌ Posts listing failed"
    echo "$LIST_RESPONSE"
fi

# Test 4: Create a comment
echo ""
echo "💬 Testing comment creation..."
COMMENT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/comments/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d "{
    \"post\": $POST_ID,
    \"content\": \"This is a test comment created via curl!\"
  }")

if echo "$COMMENT_RESPONSE" | grep -q "id"; then
    COMMENT_ID=$(echo "$COMMENT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    echo "✅ Comment created successfully"
    echo "Comment ID: $COMMENT_ID"
else
    echo "❌ Comment creation failed"
    echo "$COMMENT_RESPONSE"
fi

# Test 5: Get post with comments
echo ""
echo "🔍 Testing post detail with comments..."
DETAIL_RESPONSE=$(curl -s -X GET "$BASE_URL/api/posts/$POST_ID/" \
  -H "Authorization: Token $TOKEN")

if echo "$DETAIL_RESPONSE" | grep -q "comments"; then
    COMMENTS_COUNT=$(echo "$DETAIL_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['comments_count'])")
    echo "✅ Post detail retrieved successfully"
    echo "Comments count: $COMMENTS_COUNT"
else
    echo "❌ Post detail retrieval failed"
    echo "$DETAIL_RESPONSE"
fi

# Test 6: Search posts
echo ""
echo "🔍 Testing post search..."
SEARCH_RESPONSE=$(curl -s -X GET "$BASE_URL/api/posts/?search=curl" \
  -H "Authorization: Token $TOKEN")

if echo "$SEARCH_RESPONSE" | grep -q "results"; then
    SEARCH_COUNT=$(echo "$SEARCH_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['count'])")
    echo "✅ Post search successful"
    echo "Search results: $SEARCH_COUNT posts found"
else
    echo "❌ Post search failed"
    echo "$SEARCH_RESPONSE"
fi

echo ""
echo "🏁 All tests completed!"
echo "==========================================="
