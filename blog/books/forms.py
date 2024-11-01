from django import forms
from typing import Any
from .models import Book, Author, Publisher


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def clean(self):
        email = self.cleaned_data.get('email')
        
        if not email.endswith('@example.com'):
            raise forms.ValidationError('Email should end with @example.com')
        return email
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','description', 'author', 'publisher', 'publication_date', 'price']
        
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price should be positive')
        return price