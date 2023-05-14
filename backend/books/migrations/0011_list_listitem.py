# Generated by Django 4.2 on 2023-05-14 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0010_author_portrait_author_user_book_pages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='название')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='описание')),
                ('is_public', models.BooleanField(default=False, verbose_name='публичный')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='изменен')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lists_created', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'список',
                'verbose_name_plural': 'списки',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=1, verbose_name='номер в списке')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='описание')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создана')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='изменена')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='list_items', to='books.book', verbose_name='книга')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='books.list', verbose_name='список')),
            ],
            options={
                'verbose_name': 'элемент списка',
                'verbose_name_plural': 'элементы списков',
                'ordering': ['list', 'position'],
            },
        ),
    ]