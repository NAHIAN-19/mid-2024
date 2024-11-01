from datetime import date
from django.db import models
from django.core.validators import RegexValidator
# One to Many relations with Book
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name

# Many to One relations with Author
class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    publication_date = models.DateField(default=date.today)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Permission required to add new book details
    class Meta:
        permissions = [
            ("can_add_books", "Can add new books"),
        ]
        
    def __str__(self):
        return self.title
    
    # Class specific method to calculate book price average using Avg function
    @classmethod
    def calculate_avg_price(cls):
        return Book.objects.aggregate(models.Avg('price'))['price__avg']
    
# One to Many relations with Book
class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    established_date = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Enter a valid phone number (10-15 digits) with an optional leading '+' sign."
            )
        ]
    )
    def __str__(self):
        return self.name
    
"""
(1) Get all books by specific author:
    author_details = Author.objects.get(name='Leo Tolstoy')
    books_by_author = Book.objects.filter(author=author_details)
    for book in books_by_author:
        print(f"{book.author} : {book.title} : {book.price}")
        
(2) Find the publisher with the highest number of books.
    from django.db.models import Count
    highest_book_by_publisher = Publisher.objects.annotate(books_count=Count('book')).order_by('-books_count').first()
    print(f"{highest_book_by_publisher.name} : {highest_book_by_publisher.books_count}")

(3) Calculate the total number of books published in the last year.
    from datetime import date, timedelta
    one_year_ago = date.today() - timedelta(days=365)
    books_published_one_year_ago = Book.objects.filter(published_date__gte=one_year_ago)
    for book in books_published_one_year_ago:
        print(f"{book.author} : {book.title} : {book.publication_date}")
        
    
"""