# Generated by Django 4.2.6 on 2024-08-08 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_rename_users_recommendation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='recommendation_text',
        ),
    ]
