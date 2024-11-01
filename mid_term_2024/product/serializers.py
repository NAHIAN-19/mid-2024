from rest_framework import serializers
from product.models import Product

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    # custom validation for ProductSerializer
    def validate(self, data):
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')
        
        # name should be less than 100 characters
        if name and len(name) > 100:
            raise serializers.ValidationError("Name should be less than 100 characters")
        # price should be between 100 to 10000
        if price and price < 0:
            raise serializers.ValidationError("Price cannot be negative")
        # stock should be minimum 0
        if stock and stock < 0:
            raise serializers.ValidationError("Stock should be minimum 0")