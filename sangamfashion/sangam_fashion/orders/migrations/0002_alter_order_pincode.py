# Generated by Django 5.0.2 on 2024-02-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pincode',
            field=models.CharField(default='000000', max_length=6),
        ),
    ]
