# Generated by Django 4.2 on 2023-05-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="images/profiles/",
                verbose_name="изображение профиля",
            ),
        ),
    ]
