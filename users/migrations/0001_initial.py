# Generated by Django 5.1.7 on 2025-04-30 17:13

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('admin', 'Administrator')], default='buyer', max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('credit_card_number', models.CharField(default='0000000000000000', max_length=20)),
                ('expiration_date', models.CharField(default='01/23', max_length=7)),
                ('security_code', models.CharField(default='000', max_length=5)),
                ('street_address', models.CharField(default='Unknown Address', max_length=255)),
                ('city', models.CharField(default='Unknown', max_length=100)),
                ('state', models.CharField(default='Unknown', max_length=100)),
                ('zip_code', models.CharField(default='00000', max_length=10)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(default='Unknown', max_length=100)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('order_status', models.CharField(choices=[('delivered', 'Delivered'), ('shipped', 'Shipped'), ('ordered', 'Ordered')], default='ordered', max_length=20)),
                ('order_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('shipping_street_address', models.CharField(default='Unknown Address', max_length=255)),
                ('shipping_city', models.CharField(default='Unknown', max_length=100)),
                ('shipping_state', models.CharField(default='Unknown', max_length=100)),
                ('shipping_zip_code', models.CharField(default='00000', max_length=10)),
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('ordertime', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomShoppingCart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item_photo', models.ImageField(default='images/default.jpg', upload_to='images/')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('item_description', models.TextField()),
                ('item_snapshot_id', models.IntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('vendor_id', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='users.customorder')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('item_description', models.TextField()),
                ('item_snapshot_id', models.IntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('vendor_id', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='users.customshoppingcart')),
            ],
        ),
    ]
