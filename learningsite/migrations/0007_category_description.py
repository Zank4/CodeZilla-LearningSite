# Generated by Django 5.1.7 on 2025-05-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learningsite', '0006_remove_category_is_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default='', max_length=300),
        ),
    ]
