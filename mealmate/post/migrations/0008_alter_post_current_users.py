# Generated by Django 5.0.3 on 2024-03-23 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_remove_post_owner_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='current_users',
            field=models.TextField(blank=True, default=[], null=True),
        ),
    ]