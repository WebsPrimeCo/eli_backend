from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

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
    slug = models.SlugField(allow_unicode=True, unique=True)
    available_colors = models.ManyToManyField('Color', blank=True)
    inventory = models.PositiveIntegerField()
    descriptions = models.TextField()
    price = models.PositiveSmallIntegerField()

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)

class Comment(models.Model):
    RATE_RANK_FOR_PERFECT = 'p'
    RATE_RANK_FOR_GOOD = 'g'
    RATE_RANK_FOR_NORMAL = 'n'
    RATE_RANK_FOR_NOT_BAD = 'nb'
    RATE_RANK_FOR_BAD = 'b'

    RATE_CHOICE = [
        (RATE_RANK_FOR_PERFECT, _('Perfect')),
        (RATE_RANK_FOR_GOOD, _('Good')),
        (RATE_RANK_FOR_NORMAL, _('Normal')),
        (RATE_RANK_FOR_NOT_BAD, _('Not Bad')),
        (RATE_RANK_FOR_BAD, _('Bad')),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    
    rate = models.CharField(max_length=2, choices=RATE_CHOICE)
    body = models.TextField()
    is_active = models.BooleanField(default=True)

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)





