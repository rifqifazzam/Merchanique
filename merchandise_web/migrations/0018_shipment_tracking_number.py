# Generated by Django 4.1.7 on 2023-04-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchandise_web', '0017_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]