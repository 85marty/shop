# Generated by Django 5.1.2 on 2024-10-31 19:58

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=products.models.random_hash_filename),
        ),
    ]
