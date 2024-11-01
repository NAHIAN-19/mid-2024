# books app imports
from books.forms import BookForm, ContactForm
from books.models import Author, Book, Publisher
from books.serializers import (AuthorSerializer, BookSerializer,
                                PublisherSerializer)
# Django imports
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView, ListView
from django.views.decorators.csrf import csrf_exempt

# Rest framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


# API Based views
# Api views for Book details
class APIBookView(APIView):
    permission_classes = [IsAuthenticated]  # Set permission class for API view
    # Get method to retrive Book data by id or bulk
    def get(self, request, pk=None):
        print(request.user)
        if pk:                                           # Check if primary key is given or not
            try:
                book = Book.objects.get(pk=pk)               # Fetch Book object using primary key
                serializer = BookSerializer(book)            # Pass book object to Serializer
                return Response(serializer.data, status=status.HTTP_200_OK) # show the serializer data with Ok status
            # Return 404 status if book not found
            except Book.DoesNotExist:
                return Response({"error": "Book not found."},status=status.HTTP_404_NOT_FOUND)
        books = Book.objects.all()                       # Fetch Book objects
        serializer = BookSerializer(books, many=True)    # Pass book objects to Serializer
        return Response(serializer.data, status=status.HTTP_200_OK)  # show the serializer data with Ok status
    # Post Method to Insert Book data
    def post(self, request):
        # Pass the new Book data to serializer
        serializer = BookSerializer(data=request.data)
        # Check if all fields are valid or not
        if serializer.is_valid():
            # Save if valid
            serializer.save()                            
            # Return Ok status and new data if data is valid
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        # Return Bad request status if data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Patch method to partially update a book by id
    def patch(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)  # Find the book by primary key
        except Book.DoesNotExist:
            return Response({"error": "Book not found."},status=status.HTTP_404_NOT_FOUND)
        # Use partial update, only update provided fields
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return validation errors if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete method to delete a book by ID
    def delete(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)  # Find the book by primary key
        except Book.DoesNotExist:
            return Response({"error": "Book not found."},status=status.HTTP_404_NOT_FOUND)
        book.delete()  # Delete the book from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # No content response

# API views for Author details
class APIAuthorView(APIView):
    # Get method to retrieve Author data by id or all authors
    def get(self, request, pk=None):
        if pk:  # Check if primary key is given for a specific author
            try:
                author = Author.objects.get(pk=pk)  # Retrieve Author object using primary key
            except Author.DoesNotExist:
                # Return JSON response with 404 status if author not found
                return Response({"error": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = AuthorSerializer(author)  # Serialize single author object
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data with OK status
        
        # Retrieve all authors if no primary key is provided
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)  # Serialize multiple authors
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post method to add a new author
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)  # Pass new Author data to serializer
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save new author if valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

    # Patch method to partially update an author by id
    def patch(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk)  # Retrieve Author object by primary key
        except Author.DoesNotExist:
            return Response({"error": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
        # Serialize with partial update for provided fields only
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save updated author data if valid
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

    # Delete method to remove an author by id
    def delete(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk)  # Retrieve Author object by primary key
        except Author.DoesNotExist:
            return Response({"error": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
        author.delete()  # Delete author from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content response after deletion
    
# API views for Publisher details
class APIPublisherView(APIView):
    # Get method to retrieve Publisher data by id or all publishers
    def get(self, request, pk=None):
        if pk:  # Check if primary key is given for a specific publisher
            try:
                publisher = Publisher.objects.get(pk=pk)  # Retrieve Publisher object by primary key
            except Publisher.DoesNotExist:
                # Return JSON response with 404 status if publisher not found
                return Response({"error": "Publisher not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = PublisherSerializer(publisher)  # Serialize single publisher object
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data with OK status

        # Retrieve all publishers if no primary key is provided
        publishers = Publisher.objects.all()
        serializer = PublisherSerializer(publishers, many=True)  # Serialize multiple publishers
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Post method to add a new publisher
    def post(self, request):
        serializer = PublisherSerializer(data=request.data)  # Pass new Publisher data to serializer
        if serializer.is_valid():  # Validate the data
            serializer.save()  # Save new publisher if valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

    # Patch method to partially update a publisher by id
    def patch(self, request, pk=None):
        try:
            publisher = Publisher.objects.get(pk=pk)  # Retrieve Publisher object by primary key
        except Publisher.DoesNotExist:
            return Response({"error": "Publisher not found."}, status=status.HTTP_404_NOT_FOUND)
        # Serialize with partial update for provided fields only
        serializer = PublisherSerializer(publisher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save updated publisher data if valid
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid

    # Delete method to remove a publisher by id
    def delete(self, request, pk=None):
        try:
            publisher = Publisher.objects.get(pk=pk)  # Retrieve Publisher object by primary key
        except Publisher.DoesNotExist:
            return Response({"error": "Publisher not found."}, status=status.HTTP_404_NOT_FOUND)
        publisher.delete()  # Delete publisher from the database
        return Response(status=status.HTTP_204_NO_CONTENT)  # Return no content response after deletion

# API views using Mixins
class BookGetUpdateDelete(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Book.objects.all()  # Retrieve all books
    serializer_class = BookSerializer  # Serialize book data

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)  # Retrieve book data by primary key

    def put(self, request, *args, **kwargs):  # Update book data by primary key
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)  # Partial update book data by primary key

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)  # Delete book data by primary key

# Publisher API view using api_view decorator
class PublisherHandler:
    @api_view(['GET', 'POST'])
    @csrf_exempt
    def publishers_handler(request):
        # Get method to fetch all publishers data
        if request.method == 'GET':
            publishers = Publisher.objects.all()
            serializer = PublisherSerializer(publishers, many=True)
            # Return serialized data with Ok status
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Post method to add a new publisher
        elif request.method == 'POST':
            serializer = PublisherSerializer(data=request.data)
            # Check if data is valid
            if serializer.is_valid():
                serializer.save()
                # Return created data with Created status
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Return validation errors if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Get, Put, Patch, Delete methods for single publisher data
    @csrf_exempt
    @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
    def publisher_handler(request, pk):
        try:
            publisher = Publisher.objects.get(pk=pk)
        except Publisher.DoesNotExist:
            return Response({"error": "Publisher not found."}, status=status.HTTP_404_NOT_FOUND)
        # Get method to fetch single publisher data if id is valid
        if request.method == 'GET':
            serializer = PublisherSerializer(publisher)
            # Return serialized data with Ok status
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Put method to update single publisher data if id is valid
        elif request.method == 'PUT':
            serializer = PublisherSerializer(publisher, data=request.data)
            # Check if data is valid
            if serializer.is_valid():
                serializer.save()
                # Return updated data with Ok status
                return Response(serializer.data, status=status.HTTP_200_OK)
            # Return validation errors if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Patch method to partially update single publisher data if id is valid
        elif request.method == 'PATCH':
            serializer = PublisherSerializer(publisher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                # Return updated data with Ok status
                return Response(serializer.data, status=status.HTTP_200_OK)
            # Return validation errors if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Delete method to delete single publisher data if id is valid
        elif request.method == 'DELETE':
            publisher.delete()
            # Return no content response after successful deletion
            return Response(status=status.HTTP_204_NO_CONTENT)
        
# For publisher create api view using @api_view decorator(get, post, put, patch, delete)

# ORM based views
# Introduction to Class based view
class MyView(View):
    # Get method to show http response using 2 arguments 
    def get(self, request):
        return HttpResponse('Welcome to Django from Class!')    

# Class based view using form validation
class ContactFormView(FormView):
    # Template name to render the form
    template_name = 'contact.html'
    # Form class to validate the form
    form_class = ContactForm
    # Success url to redirect after form submission
    success_url = reverse_lazy('contact_success')
    # Show http response after form validation
    def form_valid(self, form) -> HttpResponse:
        return super().form_valid(form)
    
# Add New Book details using Model form validation
class BookAddView(PermissionRequiredMixin, CreateView): 
    model = Book                                # Model name to add new book details   
    form_class = BookForm                       # Form class to validate the form
    template_name = 'books/books_add.html'      # Template name to render the form
    success_url = reverse_lazy('book_list')     # Success url to redirect after form submission
    permission_required = 'books.can_add_books' # Permission required to add new book details
    
    def no_permission(self):
        """
            To add permission to user:
            from django.contrib.auth.models import Permission, User
            user = User.objects.get(username="nahian")
            permission = Permission.objects.get(codename="can_add_books")
            user.user_permissions.add(permission)
        """
        return HttpResponseForbidden("You do not have permission to add a book.")
    # Show http response after form validation
    def form_valid(self, form) -> HttpResponse:
        return super().form_valid(form)
    

# Return All Book details
class BookListView(ListView):
    model = Book                            # Model name to show all book details                
    template_name = 'books/books_list.html' # Template name to render the form
    
    # context to use the objects of Book model in template
    context_object_name = 'books'    
    




# python generator, threading, asyn, syn, DRY, WAIT, KISS, slug, slugify, slugfield, args, kwargs, *args, **kwargs,
# "New" function before __init__
# Q, F, Sum, Count, Avg, Prefetch(for many to many), select_related(for one to many)
# Https status code
# Html template tags
# GenericAPIView  -> Pagination
# Curl, jwt, classmethod
# Hw : viewset