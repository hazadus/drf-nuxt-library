# Generated by Django 4.2 on 2023-05-29 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_list_listitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listitem',
            options={'ordering': ['order'], 'verbose_name': 'элемент списка', 'verbose_name_plural': 'элементы списков'},
        ),
        migrations.AddField(
            model_name='listitem',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
    ]
