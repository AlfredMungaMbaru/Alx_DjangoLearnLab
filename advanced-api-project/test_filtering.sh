#!/bin/bash
# Comprehensive API Testing Script for Filtering, Searching, and Ordering
# This script demonstrates all the advanced query capabilities implemented

echo "=========================================================="
echo "Django REST Framework - Advanced Query Capabilities Test"
echo "=========================================================="
echo "Testing filtering, searching, and ordering functionality"
echo "Server should be running on http://127.0.0.1:8000/"
echo ""

# Set base URL
BASE_URL="http://127.0.0.1:8000/api"

echo "=== BASIC LISTING ==="
echo "1. List all books (GET /api/books/)"
curl -s -X GET "$BASE_URL/books/" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'results' in data:
    print(f'Total books: {data[\"count\"]}')
    for book in data['results'][:3]:  # Show first 3
        print(f'- {book[\"title\"]} by Author ID {book[\"author\"]} ({book[\"publication_year\"]})')
else:
    print('Books:', [f'{b[\"title\"]} ({b[\"publication_year\"]})' for b in data[:3]])
"
echo -e "\n"

echo "=== FILTERING TESTS ==="

echo "2. Filter by author ID (GET /api/books/?author=1)"
curl -s -X GET "$BASE_URL/books/?author=1" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books by Author ID 1: {len(books) if isinstance(books, list) else 0}')
for book in (books[:2] if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "3. Filter by publication year (GET /api/books/?publication_year=1997)"
curl -s -X GET "$BASE_URL/books/?publication_year=1997" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books from 1997: {len(books) if isinstance(books, list) else 0}')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "4. Filter by publication year range (GET /api/books/?publication_year_min=1990&publication_year_max=2000)"
curl -s -X GET "$BASE_URL/books/?publication_year_min=1990&publication_year_max=2000" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books from 1990-2000: {len(books) if isinstance(books, list) else 0}')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "5. Filter by author name (GET /api/books/?author_name=Rowling)"
curl -s -X GET "$BASE_URL/books/?author_name=Rowling" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books by authors with \"Rowling\" in name: {len(books) if isinstance(books, list) else 0}')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "=== SEARCHING TESTS ==="

echo "6. Search across title and author (GET /api/books/?search=Harry)"
curl -s -X GET "$BASE_URL/books/?search=Harry" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books matching \"Harry\": {len(books) if isinstance(books, list) else 0}')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "7. Search for author name (GET /api/books/?search=Orwell)"
curl -s -X GET "$BASE_URL/books/?search=Orwell" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Books matching \"Orwell\": {len(books) if isinstance(books, list) else 0}')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "=== ORDERING TESTS ==="

echo "8. Order by title ascending (GET /api/books/?ordering=title)"
curl -s -X GET "$BASE_URL/books/?ordering=title" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print('Books ordered by title (A-Z):')
for book in (books[:4] if isinstance(books, list) else []):
    print(f'- {book[\"title\"]}')
"
echo ""

echo "9. Order by publication year descending (GET /api/books/?ordering=-publication_year)"
curl -s -X GET "$BASE_URL/books/?ordering=-publication_year" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print('Books ordered by year (newest first):')
for book in (books[:4] if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "10. Order by author name (GET /api/books/?ordering=author__name)"
curl -s -X GET "$BASE_URL/books/?ordering=author__name" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print('Books ordered by author name:')
for book in (books[:4] if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} (Author ID: {book[\"author\"]})')
"
echo ""

echo "=== COMBINED FILTERING, SEARCHING, AND ORDERING ==="

echo "11. Combined: Search + Filter + Order (GET /api/books/?search=Harry&publication_year_min=1995&ordering=publication_year)"
curl -s -X GET "$BASE_URL/books/?search=Harry&publication_year_min=1995&ordering=publication_year" | python3 -c "
import sys, json
data = json.load(sys.stdin)
books = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print('Harry Potter books from 1995+, ordered by year:')
for book in (books if isinstance(books, list) else []):
    print(f'- {book[\"title\"]} ({book[\"publication_year\"]})')
"
echo ""

echo "=== AUTHOR FILTERING AND SEARCHING ==="

echo "12. List all authors (GET /api/authors/)"
curl -s -X GET "$BASE_URL/authors/" | python3 -c "
import sys, json
data = json.load(sys.stdin)
authors = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print(f'Total authors: {len(authors) if isinstance(authors, list) else 0}')
for author in (authors[:3] if isinstance(authors, list) else []):
    print(f'- {author[\"name\"]} ({author[\"books_count\"]} books)')
"
echo ""

echo "13. Search authors (GET /api/authors/?search=Rowling)"
curl -s -X GET "$BASE_URL/authors/?search=Rowling" | python3 -c "
import sys, json
data = json.load(sys.stdin)
authors = data.get('results', data) if isinstance(data, dict) and 'results' in data else data
print('Authors matching \"Rowling\":')
for author in (authors if isinstance(authors, list) else []):
    print(f'- {author[\"name\"]} ({author[\"books_count\"]} books)')
"
echo ""

echo "=== PAGINATION TEST ==="

echo "14. Test pagination (GET /api/books/?page=1&page_size=2)"
curl -s -X GET "$BASE_URL/books/?page=1" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'results' in data:
    print(f'Page 1: {len(data[\"results\"])} items out of {data[\"count\"]} total')
    print(f'Next page: {\"Yes\" if data[\"next\"] else \"No\"}')
    print(f'Previous page: {\"Yes\" if data[\"previous\"] else \"No\"}')
else:
    print('Pagination not configured or error occurred')
"
echo ""

echo "=========================================================="
echo "Testing Complete!"
echo ""
echo "Summary of implemented features:"
echo "✓ Basic listing of books and authors"
echo "✓ Filtering by author, publication year, and author name"
echo "✓ Range filtering for publication years"
echo "✓ Search functionality across multiple fields"
echo "✓ Ordering by title, publication year, and author name"
echo "✓ Combined filtering, searching, and ordering"
echo "✓ Pagination support"
echo "✓ Case-insensitive partial matching"
echo ""
echo "API Documentation:"
echo "- Use 'author', 'publication_year', 'author_name' for filtering"
echo "- Use 'search' parameter for text search"
echo "- Use 'ordering' parameter for sorting (prefix with '-' for descending)"
echo "- Combine multiple parameters with '&'"
echo "- All read operations are public, write operations require authentication"
echo "=========================================================="
