# Generated by Django 4.2 on 2023-05-01 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0008_book_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="description",
            field=models.TextField(
                blank=True, default=None, null=True, verbose_name="об авторе"
            ),
        ),
    ]
