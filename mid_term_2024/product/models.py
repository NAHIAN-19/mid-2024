from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    
