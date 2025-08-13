#!/bin/bash
# API Testing Script
# This script tests all the API endpoints to ensure they work correctly

echo "=== Django REST Framework API Testing ==="
echo "Server should be running on http://127.0.0.1:8000/"
echo ""

# Set base URL
BASE_URL="http://127.0.0.1:8000/api"

# Test 1: List all books (GET /api/books/) - Should work for everyone
echo "1. Testing Book List View (GET /api/books/)"
curl -X GET "$BASE_URL/books/" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 2: Get specific book (GET /api/books/1/) - Should work for everyone
echo "2. Testing Book Detail View (GET /api/books/1/)"
curl -X GET "$BASE_URL/books/1/" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 3: Try to create a book without authentication (POST /api/books/create/) - Should fail
echo "3. Testing Book Create View without authentication (POST /api/books/create/) - Should fail"
curl -X POST "$BASE_URL/books/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Book",
    "publication_year": 2023,
    "author": 1
  }' | python3 -m json.tool
echo -e "\n"

# Test 4: Create a book with authentication (using session auth)
echo "4. Testing Book Create View with authentication"
# First get CSRF token and session cookie
CSRF_TOKEN=$(curl -c cookies.txt -X GET "$BASE_URL/books/" | grep -o 'csrfmiddlewaretoken.*value="[^"]*"' | grep -o '[^"]*"$' | sed 's/"$//')

# Login and create book
echo "Creating book with authentication..."
curl -b cookies.txt -c cookies.txt -X POST "$BASE_URL/books/create/" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF_TOKEN" \
  -u "testuser:testpass123" \
  -d '{
    "title": "Authenticated Test Book",
    "publication_year": 2023,
    "author": 1
  }' | python3 -m json.tool
echo -e "\n"

# Test 5: Test validation - future year (should fail)
echo "5. Testing validation - future publication year (should fail)"
curl -b cookies.txt -X POST "$BASE_URL/books/create/" \
  -H "Content-Type: application/json" \
  -u "testuser:testpass123" \
  -d '{
    "title": "Future Book",
    "publication_year": 2030,
    "author": 1
  }' | python3 -m json.tool
echo -e "\n"

# Test 6: List all authors (GET /api/authors/)
echo "6. Testing Author List View (GET /api/authors/)"
curl -X GET "$BASE_URL/authors/" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 7: Get specific author with books (GET /api/authors/1/)
echo "7. Testing Author Detail View (GET /api/authors/1/)"
curl -X GET "$BASE_URL/authors/1/" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 8: Test filtering (GET /api/books/?author=1)
echo "8. Testing Book List with filtering (GET /api/books/?author=1)"
curl -X GET "$BASE_URL/books/?author=1" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 9: Test searching (GET /api/books/?search=Harry)
echo "9. Testing Book List with search (GET /api/books/?search=Harry)"
curl -X GET "$BASE_URL/books/?search=Harry" -H "Content-Type: application/json" | python3 -m json.tool
echo -e "\n"

# Test 10: Update a book (PATCH)
echo "10. Testing Book Update View (PATCH /api/books/1/update/)"
curl -b cookies.txt -X PATCH "$BASE_URL/books/1/update/" \
  -H "Content-Type: application/json" \
  -u "testuser:testpass123" \
  -d '{
    "title": "Harry Potter and the Philosophers Stone (Updated)"
  }' | python3 -m json.tool
echo -e "\n"

# Cleanup
rm -f cookies.txt

echo "=== API Testing Complete ==="
echo "Check the responses above to verify that:"
echo "- GET requests work for everyone"
echo "- POST/PUT/PATCH/DELETE require authentication"
echo "- Validation works correctly"
echo "- Filtering and searching work"
echo "- Nested serialization works for authors"
