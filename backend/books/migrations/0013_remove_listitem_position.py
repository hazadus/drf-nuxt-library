# Generated by Django 4.2 on 2023-06-07 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_alter_listitem_options_listitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listitem',
            name='position',
        ),
    ]
