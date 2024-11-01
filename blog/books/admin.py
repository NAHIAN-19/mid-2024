from django.contrib import admin
from .models import Book, Author, Publisher

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'publication_date', 'price']
    list_filter = ['author', 'publisher', 'publication_date']
    search_fields = ['title', 'author', 'publisher', 'publication_date']

admin.site.register(Book, BookAdmin)
