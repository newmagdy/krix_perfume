# Generated by Django 5.1.3 on 2025-02-28 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_product_price_product_price_100ml_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image1',
            field=models.ImageField(upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_100ml',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_50ml',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
