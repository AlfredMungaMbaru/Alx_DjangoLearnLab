# Delete Operation

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
# Output: <QuerySet []>
```

The Book instance was successfully deleted from the database. Retrieving all books confirms the deletion.
