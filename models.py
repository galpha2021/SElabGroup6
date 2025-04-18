

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

User = settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    def __str__(self):
        return self.city  # or email, or any identifier you prefer

    USER_ROLES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='buyer')
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, default="Unknown")
    credit_card_number = models.CharField(max_length=20, default="0000000000000000")  # Default to a placeholder number
    expiration_date = models.CharField(max_length=7, default="01/23")  # Default expiration date
    security_code = models.CharField(max_length=5, default="000")  # Default security code
    street_address = models.CharField(max_length=255, default="Unknown Address")
    city = models.CharField(max_length=100, default="Unknown")
    state = models.CharField(max_length=100, default="Unknown")
    zip_code = models.CharField(max_length=10, default="00000")
    username = models.CharField(max_length=15, default="00000")
    password = models.CharField(max_length=15, default="00000")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class CustomItem():
    id = models.BigAutoField(primary_key=True)
    item_name = models.CharField(max_length=100, default="Unknown")
    item_quantity = models.PositiveIntegerField()
    item_description = models.CharField(max_length=1000, default="Unknown")
    item_price = models.DecimalField(max_digits=9, decimal_places=2)
    item_vendor = models.CharField(max_length=1000)
    item_photo = models.ImageField(upload_to="./images", height_field=100, width_field=100)

class CustomOrder():
    ORDER_STATUS = (('delivered', 'Delivered'),
                    ('shipped', 'Shipped'),
                    ('ordered', 'Ordered')
                    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='ordered')
    order_cost =  models.DecimalField(max_digits=9, decimal_places=2)
    shipping_street_address = models.CharField(max_length=255, default="Unknown Address")
    shipping_city = models.CharField(max_length=100, default="Unknown")
    shipping_state = models.CharField(max_length=100, default="Unknown")
    shipping_zip_code = models.CharField(max_length=10, default="00000")
    order_id = models.PositiveIntegerField()
    arrivaltime = models.DateTimeField()

class CustomShoppingCart():
    number_items_in_cart = models.PositiveIntegerField(default=0)
    user_cart_id = models.PositiveIntegerField()
    cart_id = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    checkout_item_list = ArrayField(CustomItem)

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
