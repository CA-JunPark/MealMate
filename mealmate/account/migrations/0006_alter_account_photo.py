# Generated by Django 5.0.3 on 2024-03-23 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_account_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=models.TextField(default='MEDIA_ROOT/default_profile.png'),
        ),
    ]
