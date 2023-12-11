# Generated by Django 4.2.7 on 2023-12-11 09:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("url", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="url",
            old_name="seo_status",
            new_name="seo_check_status",
        ),
        migrations.AddField(
            model_name="url",
            name="seo_check_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
