from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Model representing an author of books.
    
    This model stores basic information about authors and serves as the 
    primary entity in a one-to-many relationship with Book model.
    Each author can have multiple books associated with them.
    """
    name = models.CharField(max_length=100, help_text="The author's full name")
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    class Meta:
        """Meta options for the Author model."""
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']


class Book(models.Model):
    """
    Model representing a book.
    
    This model stores information about books and establishes a foreign key
    relationship with the Author model. Each book is associated with one author,
    but an author can have multiple books (one-to-many relationship).
    """
    title = models.CharField(max_length=200, help_text="The title of the book")
    publication_year = models.IntegerField(help_text="The year the book was published")
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        help_text="The author of this book"
    )
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name} ({self.publication_year})"
    
    class Meta:
        """Meta options for the Book model."""
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']
        # Ensure no duplicate books by same author with same title and year
        unique_together = ['title', 'author', 'publication_year']
