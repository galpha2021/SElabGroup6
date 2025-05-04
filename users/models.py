

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils import timezone




class CustomUser(AbstractUser):
    def __str__(self):
        return self.city  # or email, or any identifier you prefer

    USER_ROLES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=15, choices=USER_ROLES, default='buyer')
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, default="Unknown")
    credit_card_number = models.CharField(max_length=20, default="0000000000000000")  # Default to a placeholder number
    expiration_date = models.CharField(max_length=7, default="01/23")  # Default expiration date
    security_code = models.CharField(max_length=5, default="000")  # Default security code
    street_address = models.CharField(max_length=255, default="Unknown Address")
    city = models.CharField(max_length=100, default="Unknown")
    state = models.CharField(max_length=100, default="Unknown")
    zip_code = models.CharField(max_length=10, default="00000")
    username = models.CharField(max_length=50, unique=True)
    country = models.CharField(max_length=100, default="Unknown")
    account_balance=models.DecimalField(max_digits=20,decimal_places=2, default=10000.00)
    #password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['email']
    pass




class CustomShoppingCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='shopping_carts')
    cart_id = models.AutoField(primary_key=True)
    total_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)


class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(CustomShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)  # Direct reference to Item
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_name(self):
        return self.item.name

    @property
    def item_price(self):
        return self.item.price

    @property
    def item_description(self):
        return self.item.description

    @property
    def item_photo_url(self):
        return self.item.item_photo.url

    @property
    def vendor_id(self):
        return self.item.vendor.id


class CustomOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='custom_orders')
    order_status = models.CharField(max_length=20, choices=[
        ('delivered', 'Delivered'),
        ('shipped', 'Shipped'),
        ('ordered', 'Ordered')
    ], default='ordered')
    order_cost = models.DecimalField(max_digits=9, decimal_places=2)
    shipping_street_address = models.CharField(max_length=255, default="Unknown Address")
    shipping_city = models.CharField(max_length=100, default="Unknown")
    shipping_state = models.CharField(max_length=100, default="Unknown")
    shipping_zip_code = models.CharField(max_length=10, default="00000")
    order_id = models.AutoField(primary_key=True)
    ordertime = models.DateTimeField(default=timezone.now)


class OrderItem(models.Model):
    order = models.ForeignKey(CustomOrder, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_name(self):
        return self.item.name

    @property
    def item_price(self):
        return self.item.price

    @property
    def item_description(self):
        return self.item.description

    @property
    def item_photo_url(self):
        return self.item.item_photo.url

    @property
    def vendor_id(self):
        return self.item.vendor.id

class Item(models.Model):
    User = get_user_model()
    item_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="No description")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    item_photo = models.ImageField(
    upload_to="images/",
    default="images/default.jpg"
    )
def __str__(self):
    return self.name
