# Generated by Django 4.2.6 on 2024-08-08 16:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_book_publisheddate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='user',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
