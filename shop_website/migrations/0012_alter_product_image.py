# Generated by Django 5.0.7 on 2024-08-03 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_website', '0011_alter_order_phone_number_alter_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='sample_image.pg', upload_to='products'),
        ),
    ]
