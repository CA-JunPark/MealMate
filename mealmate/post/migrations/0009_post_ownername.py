# Generated by Django 4.2 on 2024-04-09 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_post_current_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ownerName',
            field=models.CharField(default='', max_length=30),
        ),
    ]
