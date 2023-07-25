# Generated by Django 4.2.1 on 2023-07-22 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_users_product_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerproductprice',
            name='inventory',
            field=models.PositiveBigIntegerField(default=50000, help_text='Please Enter the Number of this Product Item into the Stock', verbose_name='Number of Inventory'),
            preserve_default=False,
        ),
    ]
