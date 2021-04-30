from django.urls import path, include
from . import views  
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('books/<int:book_id>', views.books_id),
    path('books/ad', views.books_ad),
    path('books/<int:book_id>/update', views.books_id_update),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('books/<int:book_id>/eliminate', views.eliminate),
    
]