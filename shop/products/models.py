import hashlib
import os

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


def random_hash_filename(instance, filename):
    # Generuj náhodný hash
    hash_name = hashlib.md5(filename.encode()).hexdigest()
    extension = os.path.splitext(filename)[1]
    return f'static/products/images/{hash_name}{extension}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to=random_hash_filename, blank=True)
