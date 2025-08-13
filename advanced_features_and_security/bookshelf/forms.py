from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN (13 digits)'
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text
        self.fields['isbn'].help_text = 'Enter the 13-digit ISBN number'
        self.fields['publication_date'].help_text = 'Select the publication date'
    
    def clean_isbn(self):
        """
        Validate ISBN format.
        """
        isbn = self.cleaned_data.get('isbn')
        if isbn and len(isbn) != 13:
            raise forms.ValidationError('ISBN must be exactly 13 digits long.')
        if isbn and not isbn.isdigit():
            raise forms.ValidationError('ISBN must contain only digits.')
        return isbn
