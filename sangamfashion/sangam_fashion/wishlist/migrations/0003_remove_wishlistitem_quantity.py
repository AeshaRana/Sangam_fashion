# Generated by Django 5.0.2 on 2024-02-13 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wishlistitem_user_alter_wishlistitem_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlistitem',
            name='quantity',
        ),
    ]
