# Generated by Django 4.2 on 2025-01-20 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_django_app', '0002_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, to='my_django_app.role'),
        ),
    ]
