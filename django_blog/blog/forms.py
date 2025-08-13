from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    """Extended user registration form with email field"""
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name (optional)'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name (optional)'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to existing fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user profile information"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None


class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts with django-taggit integration"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your post title...',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 15,
                'style': 'resize: vertical;'
            }),
            'tags': TagWidget(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas (e.g., django, python, web)',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'top',
                'title': 'Enter tags separated by commas'
            })
        }
        help_texts = {
            'title': 'Maximum 200 characters.',
            'content': 'Write your blog post content. You can use line breaks for paragraphs.',
            'tags': 'Enter tags separated by commas. Tags help categorize your post.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Maximum 200 characters.'
        self.fields['content'].help_text = 'Write your blog post content. You can use line breaks for paragraphs.'
        self.fields['tags'].help_text = 'Enter tags separated by commas. Tags help categorize your post.'
        
        # Pre-populate tags field if editing existing post
        if self.instance and self.instance.pk:
            tags = self.instance.tags.all()
            if tags:
                self.fields['tags_input'].initial = ', '.join([tag.name for tag in tags])

    def save(self, commit=True):
        """Save the post and handle tags"""
        post = super().save(commit=commit)
        
        if commit:
            # Clear existing tags
            post.tags.clear()
            
            # Process new tags
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [name.strip().lower() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    if tag_name:  # Only process non-empty tags
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag)
        
        return post

    def clean_title(self):
        """Validate the title field"""
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError('Title is required.')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean_content(self):
        """Validate the content field"""
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Content is required.')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts...',
                'required': True
            })
        }
        labels = {
            'content': 'Comment'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control'
        })
    
    def clean_content(self):
        """Validate the comment content"""
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError('Comment content is required.')
        if len(content.strip()) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return content.strip()


class SearchForm(forms.Form):
    """Form for searching blog posts"""
    query = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts by title, content, or tags...',
            'aria-label': 'Search'
        }),
        help_text='Search for posts by title, content, or tags'
    )

    def clean_query(self):
        """Validate and clean the search query"""
        query = self.cleaned_data.get('query')
        if query:
            query = query.strip()
            if len(query) < 2:
                raise forms.ValidationError('Search query must be at least 2 characters long.')
        return query
