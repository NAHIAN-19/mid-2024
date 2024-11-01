# Django imports for path and views
from django.shortcuts import render
from django.urls import path
# Importing views from books app
from books.views import (APIAuthorView, APIBookView, APIPublisherView, BookAddView,
                        BookListView, BookGetUpdateDelete, ContactFormView, MyView, PublisherHandler)


urlpatterns = [
    # Initial class based view urls
    path('initial_class/', MyView.as_view(), name='initial_class'),
    
    # Books related urls
    path('add/', BookAddView.as_view(), name='book_add'),
    path('list/', BookListView.as_view(), name='book_list'),
    
    # Contact form related urls
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('contact_success/', lambda request: render(request,'success/contact_success.html'), name='contact_success'),
    
    # Rest api urls
    path('api/books/', APIBookView.as_view(), name='api_books'), # Book List and Create
    path('api/books/<int:pk>/', APIBookView.as_view(), name='api_book'), # Book Retrieve, Update and Delete
    path('api/authors/', APIAuthorView.as_view(), name='api_authors'), # Author List and Create
    path('api/authors/<int:pk>/', APIAuthorView.as_view(), name='api_author'), # Author Retrieve, Update and Delete
    path('api/publishers/', APIPublisherView.as_view(), name='api_publishers'), # Publisher List and Create
    path('api/publishers/<int:pk>/', APIPublisherView.as_view(), name='api_publisher'), # Publisher Retrieve, Update and Delete
    
    # Rest api urls using Mixins
    path('rest/book/<int:pk>/', BookGetUpdateDelete.as_view(), name='rest_books'), # Book List and Create
    
    # Rest api urls using Decorators
    path('rest/publishers/', PublisherHandler.publishers_handler, name='rest_publishers'), # Publishers Data Handler using decorator
    path('rest/publisher/<int:pk>/', PublisherHandler.publisher_handler, name='rest_publisher'), # Publisher Data Handler using decorator
    
]