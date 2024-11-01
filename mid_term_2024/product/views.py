from django.shortcuts import render

# create a simple API endpoint for searching products by name in drf. the endpoint should accept a query parameter  and filter the Product model to return matching results.
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerializer


class ProductApiView(APIView):
    # receive a query parameter and filter the Product model to return matching results
    def get(self, request, query=None):
        query = request.query_params.get('query')
        if query:
            # filter the query param to search in each field
            products_by_name = Product.objects.filter(name__icontains=query)
            products_by_description = Product.objects.filter(description__icontains=query)
            products_by_price = Product.objects.filter(price__icontains=query)
            products_by_stock = Product.objects.filter(stock__icontains=query)
            # combine the results
            products = products_by_name | products_by_description | products_by_price | products_by_stock
            # serialize the results
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            if products:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"Error": "Product not found!"},status=status.HTTP_204_NO_CONTENT)
        

