# Generated by Django 5.0.1 on 2024-02-28 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0005_review_application_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='Total_Price',
            field=models.IntegerField(default=100),
        ),
    ]
