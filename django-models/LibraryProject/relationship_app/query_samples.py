from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

# Example usage (uncomment to run in Django shell):
# print(books_by_author('John Doe'))
# print(books_in_library('Central Library'))
# print(librarian_for_library('Central Library'))
