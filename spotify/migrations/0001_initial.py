# Generated by Django 5.2 on 2025-06-28 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Credential",
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
                ("cliend_id", models.CharField(max_length=32)),
                ("client_secret", models.CharField(max_length=32)),
            ],
        ),
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
                ("creation_time", models.DateTimeField(auto_now_add=True)),
                ("expires_in", models.IntegerField()),
            ],
        ),
    ]
