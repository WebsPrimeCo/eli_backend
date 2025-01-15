import factory
import factory.fuzzy
from faker import Faker
from store.models import (
    Category, Discount, Product, Color, Size, Comment, Customer, Order, OrderItem
)

fake = Faker()

# -----------------------------------------------------------------------------
# 1. Category Factory
# -----------------------------------------------------------------------------
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker('sentence', nb_words=2)  # مثل "Electronics"
    description = factory.Faker('text', max_nb_chars=100)
    top_product = None

# -----------------------------------------------------------------------------
# 2. Discount Factory
# -----------------------------------------------------------------------------
class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    discount = factory.fuzzy.FuzzyDecimal(0, 50, precision=1)
    description = factory.Faker('sentence', nb_words=4)

# -----------------------------------------------------------------------------
# 3. Color Factory
# -----------------------------------------------------------------------------
class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Color

    name = factory.Faker('color_name')  # مثل "Red"
    code = factory.Faker('hex_color')  # مثل "#FF0000"

# -----------------------------------------------------------------------------
# 4. Size Factory
# -----------------------------------------------------------------------------
class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    size = factory.fuzzy.FuzzyChoice(['S', 'M', 'L', 'XL', 'XXL'])

# -----------------------------------------------------------------------------
# 5. Product Factory
# -----------------------------------------------------------------------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    image_1 = factory.django.ImageField(color='blue')
    image_2 = factory.django.ImageField(color='green')
    image_3 = factory.django.ImageField(color='red')
    title = factory.Faker('word')
    slug = factory.Faker('slug')
    inventory = factory.fuzzy.FuzzyInteger(1, 100)
    descriptions = factory.Faker('paragraph', nb_sentences=3)
    price = factory.fuzzy.FuzzyDecimal(10, 1000, precision=2)
    create_at = factory.Faker('date_time_this_year')
    modified_at = factory.Faker('date_time_this_year')

    @factory.post_generation
    def available_colors(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for color in extracted:
                self.available_colors.add(color)
        else:
            self.available_colors.add(ColorFactory())

    @factory.post_generation
    def available_size(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for size in extracted:
                self.available_size.add(size)
        else:
            self.available_size.add(SizeFactory())

# -----------------------------------------------------------------------------
# 6. Comment Factory
# -----------------------------------------------------------------------------
class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory('myapp.factories.UserFactory')  # جایگزین UserFactory با مدل کاربرتان
    product = factory.SubFactory(ProductFactory)
    rate = factory.fuzzy.FuzzyChoice([rate[0] for rate in Comment.RATE_CHOICE])
    body = factory.Faker('paragraph', nb_sentences=2)
    status = factory.fuzzy.FuzzyChoice([status[0] for status in Comment.COMMENT_STATUS])

# -----------------------------------------------------------------------------
# 7. Customer Factory
# -----------------------------------------------------------------------------
class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    birth_date = factory.Faker('date_of_birth')
    province = factory.Faker('state')
    city = factory.Faker('city')
    street = factory.Faker('street_address')

# -----------------------------------------------------------------------------
# 8. Order Factory
# -----------------------------------------------------------------------------
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomerFactory)
    datetime_created = factory.Faker('date_time_this_year')
    status = factory.fuzzy.FuzzyChoice([status[0] for status in Order.ORDER_STATUS])

# -----------------------------------------------------------------------------
# 9. OrderItem Factory
# -----------------------------------------------------------------------------
class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.fuzzy.FuzzyInteger(1, 10)
    unit_price = factory.LazyAttribute(lambda o: o.product.price)

