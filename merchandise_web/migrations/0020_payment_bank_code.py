# Generated by Django 4.1.7 on 2023-04-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise_web', '0019_order_virtual_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='bank_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
