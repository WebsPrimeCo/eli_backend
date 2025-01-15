from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, related_name='+')

class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_1 = models.ImageField(upload_to='media/product_cover/', blank=True)
    image_2 = models.ImageField(upload_to='media/product_cover/', blank=True)
    image_3 = models.ImageField(upload_to='media/product_cover/')
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True, unique=True)
    available_colors = models.ManyToManyField('Color', blank=True)
    available_size = models.ManyToManyField('Size', blank=True)
    inventory = models.PositiveIntegerField()
    descriptions = models.TextField()
    price = models.PositiveSmallIntegerField()

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)

class Size(models.Model):
    size = models.CharField(max_length=10)

class Comment(models.Model):
    RATE_RANK_FOR_PERFECT = 'p'
    RATE_RANK_FOR_GOOD = 'g'
    RATE_RANK_FOR_NORMAL = 'n'
    RATE_RANK_FOR_NOT_BAD = 'nb'
    RATE_RANK_FOR_BAD = 'b'
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'

    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    RATE_CHOICE = [
        (RATE_RANK_FOR_PERFECT, _('Perfect')),
        (RATE_RANK_FOR_GOOD, _('Good')),
        (RATE_RANK_FOR_NORMAL, _('Normal')),
        (RATE_RANK_FOR_NOT_BAD, _('Not Bad')),
        (RATE_RANK_FOR_BAD, _('Bad')),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='comments')   
    rate = models.CharField(max_length=2, choices=RATE_CHOICE)
    body = models.TextField()
    status = models.CharField(max_length=2, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Order(models.Model):
    ORDER_STATUS_PAID = 'p'
    ORDER_STATUS_UNPAID = 'u'
    ORDER_STATUS_CANCELED = 'c'
    ORDER_STATUS = [
        (ORDER_STATUS_PAID,'Paid'),
        (ORDER_STATUS_UNPAID,'Unpaid'),
        (ORDER_STATUS_CANCELED,'Canceled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
