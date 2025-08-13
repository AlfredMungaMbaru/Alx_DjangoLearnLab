from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances.
    It includes custom validation to ensure the publication_year is not in the future,
    which helps maintain data integrity for book records.
    
    Fields:
        - title: The title of the book
        - publication_year: The year the book was published (with future date validation)
        - author: Foreign key reference to the Author model
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This validation prevents users from entering unrealistic publication dates.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates advanced serialization techniques by including
    a nested relationship. It serializes the Author model along with all related
    books using the BookSerializer. This creates a hierarchical JSON structure
    that shows the author's information alongside their complete bibliography.
    
    The 'books' field uses the related_name defined in the Book model's foreign key
    relationship, which allows us to access all books by a specific author.
    
    Fields:
        - id: The unique identifier for the author
        - name: The author's full name
        - books: A nested serialization of all books written by this author
    
    Relationship Handling:
        The Author-Book relationship is handled through Django's ForeignKey with
        related_name='books'. This allows the AuthorSerializer to automatically
        serialize all related Book instances when an Author is serialized.
        
        The relationship works as follows:
        1. One Author can have many Books (one-to-many)
        2. Each Book belongs to exactly one Author
        3. The 'books' field in this serializer dynamically includes all books
           associated with the author instance being serialized
        4. The nested BookSerializer ensures proper validation and formatting
           of each book's data within the author's serialized representation
    """
    
    # Nested serialization of related books
    # The source='books' refers to the related_name in the Book model's ForeignKey
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def to_representation(self, instance):
        """
        Override to provide custom representation logic if needed.
        
        This method can be used to customize how the Author instance is
        serialized, including any post-processing of the nested books data.
        
        Args:
            instance (Author): The Author instance being serialized
            
        Returns:
            dict: The serialized representation of the Author with nested books
        """
        representation = super().to_representation(instance)
        
        # Add additional metadata about the author's books
        if 'books' in representation:
            books_count = len(representation['books'])
            representation['books_count'] = books_count
            
            # Add publication year range if books exist
            if books_count > 0:
                years = [book['publication_year'] for book in representation['books']]
                representation['publication_year_range'] = {
                    'earliest': min(years),
                    'latest': max(years)
                }
        
        return representation
