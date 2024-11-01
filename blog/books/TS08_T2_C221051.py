from django.views.generic import ListView
from .models import Book
from django.views import View
from django.http import HttpResponse


# Show book details using class based view
class BookListView(ListView):
    model = Book
    template_name = 'hello.html'
    context_object_name = 'books'

class MyView(View):
    def get(self, request):
        return HttpResponse('Welcome to Django from Class!')
    
def hello(request):
    return HttpResponse('Welcome to Django from Class!')
    
# python generator, threading, asyn, syn, DRY, WAIT, KISS, 
# New function before __init__
# Q, F, Sum, Count, Avg, Prefetch(for many to many), select_related(for one to many)
# Https status code

