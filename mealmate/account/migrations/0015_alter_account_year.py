# Generated by Django 4.2 on 2024-04-09 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_account_emailagree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='year',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
