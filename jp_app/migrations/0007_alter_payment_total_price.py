# Generated by Django 5.0.1 on 2024-02-28 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0006_payment_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='Total_Price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]