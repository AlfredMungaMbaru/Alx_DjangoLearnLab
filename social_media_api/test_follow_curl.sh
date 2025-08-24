#!/bin/bash

# Simple bash script to test Follow and Feed functionality
BASE_URL="http://127.0.0.1:8000"

echo "🚀 Testing Follow and Feed Functionality"
echo "========================================"

# Test 1: Register Alice
echo ""
echo "📝 Creating Alice..."
ALICE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_curl",
    "email": "alice_curl@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Alice via curl"
  }')

if echo "$ALICE_RESPONSE" | grep -q "token"; then
    ALICE_TOKEN=$(echo "$ALICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
    ALICE_ID=$(echo "$ALICE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['id'])")
    echo "✅ Alice created (ID: $ALICE_ID)"
else
    echo "❌ Alice creation failed, trying login..."
    ALICE_LOGIN=$(curl -s -X POST "$BASE_URL/api/accounts/login/" \
      -H "Content-Type: application/json" \
      -d '{"username": "alice_curl", "password": "testpass123"}')
    
    if echo "$ALICE_LOGIN" | grep -q "token"; then
        ALICE_TOKEN=$(echo "$ALICE_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
        ALICE_ID=$(echo "$ALICE_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['id'])")
        echo "✅ Alice logged in (ID: $ALICE_ID)"
    else
        echo "❌ Alice authentication failed"
        exit 1
    fi
fi

# Test 2: Register Bob
echo ""
echo "📝 Creating Bob..."
BOB_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob_curl",
    "email": "bob_curl@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Bob via curl"
  }')

if echo "$BOB_RESPONSE" | grep -q "token"; then
    BOB_TOKEN=$(echo "$BOB_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
    BOB_ID=$(echo "$BOB_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['id'])")
    echo "✅ Bob created (ID: $BOB_ID)"
else
    echo "❌ Bob creation failed, trying login..."
    BOB_LOGIN=$(curl -s -X POST "$BASE_URL/api/accounts/login/" \
      -H "Content-Type: application/json" \
      -d '{"username": "bob_curl", "password": "testpass123"}')
    
    if echo "$BOB_LOGIN" | grep -q "token"; then
        BOB_TOKEN=$(echo "$BOB_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])")
        BOB_ID=$(echo "$BOB_LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin)['user']['id'])")
        echo "✅ Bob logged in (ID: $BOB_ID)"
    else
        echo "❌ Bob authentication failed"
        exit 1
    fi
fi

# Test 3: Alice follows Bob
echo ""
echo "📍 Alice follows Bob..."
FOLLOW_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/follow/$BOB_ID/" \
  -H "Authorization: Token $ALICE_TOKEN")

if echo "$FOLLOW_RESPONSE" | grep -q "now following"; then
    echo "✅ Alice is now following Bob"
else
    echo "❌ Follow failed: $FOLLOW_RESPONSE"
fi

# Test 4: Bob creates a post
echo ""
echo "📝 Bob creates a post..."
POST_RESPONSE=$(curl -s -X POST "$BASE_URL/api/posts/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $BOB_TOKEN" \
  -d '{
    "title": "Bob'\''s Test Post",
    "content": "This is a test post from Bob for the feed!"
  }')

if echo "$POST_RESPONSE" | grep -q "id"; then
    echo "✅ Bob created a post"
else
    echo "❌ Post creation failed: $POST_RESPONSE"
fi

# Test 5: Alice checks her feed
echo ""
echo "📰 Alice checks her feed..."
FEED_RESPONSE=$(curl -s -X GET "$BASE_URL/api/feed/" \
  -H "Authorization: Token $ALICE_TOKEN")

if echo "$FEED_RESPONSE" | grep -q "following_count"; then
    echo "✅ Feed loaded successfully"
    echo "Feed data:"
    echo "$FEED_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Following: {data.get('following_count', 0)} users\")
    if 'results' in data:
        posts = data['results'].get('posts', [])
    else:
        posts = data.get('posts', [])
    print(f\"Posts in feed: {len(posts)}\")
    for post in posts:
        print(f\"  - '{post['title']}' by {post['author']['username']}\")
except:
    print('Error parsing feed data')
"
else
    echo "❌ Feed loading failed: $FEED_RESPONSE"
fi

# Test 6: Check following list
echo ""
echo "📋 Alice's following list..."
FOLLOWING_RESPONSE=$(curl -s -X GET "$BASE_URL/api/accounts/following/" \
  -H "Authorization: Token $ALICE_TOKEN")

if echo "$FOLLOWING_RESPONSE" | grep -q "following_count"; then
    echo "✅ Following list retrieved"
    echo "$FOLLOWING_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Following {data.get('following_count', 0)} users:\")
    for user in data.get('following', []):
        print(f\"  - {user['username']} (ID: {user['id']})\")
except:
    print('Error parsing following data')
"
else
    echo "❌ Following list failed: $FOLLOWING_RESPONSE"
fi

# Test 7: Alice unfollows Bob
echo ""
echo "📍 Alice unfollows Bob..."
UNFOLLOW_RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/unfollow/$BOB_ID/" \
  -H "Authorization: Token $ALICE_TOKEN")

if echo "$UNFOLLOW_RESPONSE" | grep -q "unfollowed"; then
    echo "✅ Alice unfollowed Bob"
else
    echo "❌ Unfollow failed: $UNFOLLOW_RESPONSE"
fi

echo ""
echo "🏁 Follow and Feed tests completed!"
echo "========================================"
