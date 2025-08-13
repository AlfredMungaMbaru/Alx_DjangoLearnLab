from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book management URLs
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/add/', views.BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Search functionality
    path('search/', views.book_search, name='book_search'),
    
    # Secure API endpoints
    path('api/search/', views.api_book_search, name='api_book_search'),
    
    # Security testing
    path('security-test/', views.security_headers_test, name='security_test'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
