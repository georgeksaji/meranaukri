# Generated by Django 5.0.1 on 2024-02-24 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0004_alter_plan_plan_description_alter_plan_plan_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='Application_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jp_app.job_application'),
        ),
    ]
