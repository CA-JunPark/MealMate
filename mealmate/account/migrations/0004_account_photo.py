# Generated by Django 5.0.3 on 2024-03-22 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='photo',
            field=models.TextField(default='media/default_profile.png'),
        ),
    ]
