from rest_framework import serializers
from books.models import Book, Author, Publisher
from datetime import datetime
    
        
# Author Serializer 
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
# Publisher Serializer 
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
    # custom validation for PublisherSerializer
    def validate(self, data):
        name = data.get('name')
        established_date = data.get('established_date')
        # name should be less than 100 characters
        if name and len(name) > 100:
            raise serializers.ValidationError("Name should be less than 100 characters")
        # established date should be minimum 1 years old
        if established_date and (datetime.now().date() - established_date).days < 365:
            raise serializers.ValidationError("Established date should be minimum 1 years old")
        return data
        
# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    """
        author and publisher are nested serializers
        to get author and publisher details in book response
    """
    author = AuthorSerializer()
    publisher = PublisherSerializer()
    class Meta:
        model = Book
        fields = '__all__'
    # custom validation for BookSerializer
    def validate(self, data):
        title = data.get('title')
        description = data.get('description')
        publication_date = data.get('publication_date')
        price = data.get('price')
        
        # title should be max 100 characters
        if title and len(title) > 100:
            raise serializers.ValidationError("Title should be less than 100 characters")
        # description should contain minimum 10 words
        if description and len(description.split()) < 10:
            raise serializers.ValidationError("Description should contain minimum 10 words")
        # publication date should be minimum 1 month old
        if publication_date:
            if (datetime.now().date() - publication_date).days < 30:
                raise serializers.ValidationError("Publication date should be minimum 1 month old")
        # price should be between 100 to 10000
        if price and (price < 100 or price > 10000):
            raise serializers.ValidationError("Price should be between 100 to 10000")
        return data
    # Custom create method for BookSerializer
    def create(self, validated_data):
        """
            to define a custom create method for BookSerializer
            that will create author, publisher and book objects,
            first create author and publisher objects
            then create book object with author and publisher objects
        """
        # author is the variable defined to call AuthorSerializer
        author_data = validated_data.pop('author')
        # publisher is the variable defined to call PublisherSerializer
        publisher_data = validated_data.pop('publisher')
        # create author and publisher objects with author_data and publisher_data
        new_author = AuthorSerializer(data=author_data)
        new_publisher = PublisherSerializer(data=publisher_data)
        if new_author.is_valid():
            new_author = new_author.save()
            validated_data['author'] = new_author
        if new_publisher.is_valid():
            new_publisher = new_publisher.save()
            validated_data['publisher'] = new_publisher
        return super().create(validated_data)
    # Custom update method for BookSerializer
    def update(self, instance, validated_data):
        
        validated_data['updated_at'] = datetime.now()
        return super().update(instance, validated_data)
# hw : create list view using rest framework Book