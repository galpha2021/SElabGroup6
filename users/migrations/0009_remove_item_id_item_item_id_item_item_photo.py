# Generated by Django 5.2 on 2025-04-15 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='id',
        ),
        migrations.AddField(
            model_name='item',
            name='item_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='item',
            name='item_photo',
            field=models.ImageField(default='images/default.jpg', upload_to='images/'),
        ),
    ]
