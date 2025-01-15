import factory
import factory.fuzzy
from faker import Faker

from .models import (
    Category,
    Discount,
    Product,
    Customer,
    Address,
    Order,
    OrderItem,
    Comment,
    Cart,
    CartItem
)

fake = Faker()

# -----------------------------------------------------------------------------
# 1. Category Factory
# -----------------------------------------------------------------------------
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('sentence', nb_words=2)   # یک جمله کوتاه مثلاً "Electronic Devices"
    description = factory.Faker('text', max_nb_chars=100)  # متن کوتاه برای توضیحات
    top_product = None
    # توجه: اگر بخواهید در top_product یک محصول خاص قرار دهید (که مرتبط با همان Category باشد)،
    # باید با احتیاط عمل کنید تا دچار حلقه (Circular Dependency) نشویم.
    # فعلاً آن را None می‌گذاریم. می‌توانید بعداً به صورت دستی یا با ترفندهای تستی مقداردهی کنید.


# -----------------------------------------------------------------------------
# 2. Discount Factory
# -----------------------------------------------------------------------------
class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    discount = factory.fuzzy.FuzzyDecimal(0, 50, precision=1)  # مثلاً عددی بین 0 تا 50 درصد تخفیف
    description = factory.Faker('sentence', nb_words=4)


# -----------------------------------------------------------------------------
# 3. Product Factory
# -----------------------------------------------------------------------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')  # نام کالا مثلاً "Laptop"
    category = factory.SubFactory(CategoryFactory)
    slug = factory.Faker('slug')
    description = factory.Faker('paragraph', nb_sentences=2)
    unit_price = factory.fuzzy.FuzzyDecimal(1, 999, precision=2)  # قیمت بین 1 تا 999
    inventory = factory.fuzzy.FuzzyInteger(0, 1000)

    # در صورت تمایل می‌توانید تخفیف‌ها را نیز اضافه کنید:
    @factory.post_generation
    def discounts(self, create, extracted, **kwargs):
        """
        اگر هنگام ساخت ProductFactory از پارامتر discounts استفاده کنیم،
        می‌توانیم تخفیف‌های دلخواهمان را اضافه کنیم:
        product = ProductFactory(discounts=[discount1, discount2, ...])
        """
        if not create:
            return
        if extracted:
            for discount in extracted:
                self.discounts.add(discount)


# -----------------------------------------------------------------------------
# 4. Customer Factory
# -----------------------------------------------------------------------------
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    # با Faker('phone_number') ممکن است فرمت آمریکایی تولید شود؛ اگر فرمت ایرانی نیاز دارید،
    # باید کاستوم بنویسید یا از "fa_IR" برای Locale استفاده کنید.
    birth_date = factory.Faker('date_of_birth')


# -----------------------------------------------------------------------------
# 5. Address Factory
# -----------------------------------------------------------------------------
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    # به دلیل OneToOne با Customer، هر Address فقط به یک Customer منحصربه‌فرد تعلق می‌گیرد.
    # در حالت پیش‌فرض زیر، هنگام ساخت Address، یک Customer جدید با SubFactory ساخته می‌شود.
    customer = factory.SubFactory(CustomerFactory)
    province = factory.Faker('state')
    city = factory.Faker('city')
    street = factory.Faker('street_address')


# -----------------------------------------------------------------------------
# 6. Order Factory
# -----------------------------------------------------------------------------
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    # یکی از وضعیت‌های ممکن را به تصادف یا نوبتی انتخاب می‌کنیم
    status = factory.Iterator([Order.ORDER_STATUS_PAID, 
                               Order.ORDER_STATUS_UNPAID, 
                               Order.ORDER_STATUS_CANCELED])


# -----------------------------------------------------------------------------
# 7. OrderItem Factory
# -----------------------------------------------------------------------------
class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)

    # به عنوان پیش‌فرض قیمت واحد را با توجه به قیمت کالا تعیین می‌کنیم.
    unit_price = factory.LazyAttribute(lambda o: o.product.unit_price)


# -----------------------------------------------------------------------------
# 8. Comment Factory
# -----------------------------------------------------------------------------
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    product = factory.SubFactory(ProductFactory)
    name = factory.Faker('name')
    body = factory.Faker('paragraph', nb_sentences=2)
    status = factory.Iterator([
        Comment.COMMENT_STATUS_WAITING,
        Comment.COMMENT_STATUS_APPROVED,
        Comment.COMMENT_STATUS_NOT_APPROVED
    ])


# -----------------------------------------------------------------------------
# 9. Cart Factory
# -----------------------------------------------------------------------------
class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart


# -----------------------------------------------------------------------------
# 10. CartItem Factory
# -----------------------------------------------------------------------------
class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)
