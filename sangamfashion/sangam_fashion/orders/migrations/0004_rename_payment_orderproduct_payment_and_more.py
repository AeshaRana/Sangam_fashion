# Generated by Django 5.0.2 on 2024-02-16 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_order_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='Payment',
            new_name='payment',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
