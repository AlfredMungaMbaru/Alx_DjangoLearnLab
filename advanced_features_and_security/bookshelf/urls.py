from django.urls import path
from . import views

urlpatterns = [
    # Function-based views
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('search/', views.book_search, name='book_search'),
    
    # Class-based views (alternative implementations)
    path('cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('cbv/create/', views.BookCreateView.as_view(), name='book_create_cbv'),
    path('cbv/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_edit_cbv'),
    path('cbv/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete_cbv'),
]
