# Generated by Django 4.2 on 2023-05-01 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_bookcard_is_reading"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="isbn",
            field=models.CharField(
                blank=True, max_length=13, null=True, verbose_name="ISBN"
            ),
        ),
    ]
