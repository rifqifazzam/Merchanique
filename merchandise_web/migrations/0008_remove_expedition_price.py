# Generated by Django 4.1.7 on 2023-04-21 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise_web', '0007_expedition_image_expedition_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expedition',
            name='price',
        ),
    ]
