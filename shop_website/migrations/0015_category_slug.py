# Generated by Django 5.0.7 on 2024-08-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_website', '0014_alter_order_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
