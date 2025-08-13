from django import forms
from .models import Book


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form handling practices.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        })
    )
    
    def clean_name(self):
        """
        Validate and sanitize the name field.
        """
        name = self.cleaned_data.get('name')
        if name:
            # Remove any potentially dangerous characters
            import re
            name = re.sub(r'[<>"\']', '', name)
            if len(name.strip()) < 2:
                raise forms.ValidationError('Name must be at least 2 characters long.')
        return name.strip()
    
    def clean_message(self):
        """
        Validate and sanitize the message field.
        """
        message = self.cleaned_data.get('message')
        if message:
            # Basic sanitization
            import re
            # Remove script tags and other potentially dangerous HTML
            message = re.sub(r'<script.*?</script>', '', message, flags=re.IGNORECASE | re.DOTALL)
            message = re.sub(r'javascript:', '', message, flags=re.IGNORECASE)
            if len(message.strip()) < 10:
                raise forms.ValidationError('Message must be at least 10 characters long.')
        return message.strip()


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
