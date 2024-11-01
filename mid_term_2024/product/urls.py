from django.urls import path
from product.views import ProductApiView
# import template view
from django.views.generic import TemplateView
urlpatterns = [
    path('api/product/', ProductApiView.as_view(), name='product_api'),
]

# filter the query param to search in each field
# localhost:8000/api/product/?query=any_query