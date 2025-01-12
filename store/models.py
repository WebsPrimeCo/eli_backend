from django.db import models
from django.utils.translation import gettext as _

class Category(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField()
    top_product = models.ForeignKey('product', on_delete=models.PROTECT, blank=True, null=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_1 = models.ImageField(upload_to='media/', blank=True)
    image_2 = models.ImageField(upload_to='media/', blank=True)
    image_3 = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    available_colors = models.ManyToManyField('Color', blank=True)
    inventory = models.PositiveIntegerField()
    descriptions = models.TextField()
    price = models.PositiveSmallIntegerField()

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)




