from django.db import models
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5


    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/products', null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1)
    rating = models.PositiveIntegerField(choices=RatingChoices.choices, default=RatingChoices.ONE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')

    @property
    def image_url(self):
        return self.image.url

    @property
    def discounted_price(self):
        if self.discount > 0:
            self.price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return Decimal(self.price).quantize(Decimal('0.001'))

    def __str__(self):
        return self.name

class Order(BaseModel):
    full_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(region='UZ')
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)