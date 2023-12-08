# Generated by Django 4.2.7 on 2023-12-08 09:44

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("url", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SeoData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("type", models.CharField(default="", max_length=255)),
                ("data", models.JSONField()),
                (
                    "url",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="seo_data",
                        to="url.url",
                    ),
                ),
            ],
            options={
                "db_table": "seo_data",
            },
        ),
    ]