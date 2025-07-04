# Generated by Django 5.2 on 2025-06-28 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spotify", "0006_delete_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
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
                ("secret", models.CharField(max_length=139)),
                ("type", models.CharField(max_length=30)),
                ("expiry_time", models.DateTimeField()),
            ],
        ),
    ]
