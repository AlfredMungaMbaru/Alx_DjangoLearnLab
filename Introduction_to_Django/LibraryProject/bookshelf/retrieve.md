# Retrieve Operation

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# Output: 1984 George Orwell 1949
```

The Book instance was successfully retrieved from the database and its attributes displayed.
