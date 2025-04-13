

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


