# Generated by Django 4.2 on 2024-04-10 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_alter_post_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='when',
            field=models.TimeField(blank=True, default='2024-04-09 12:08:00', null=True),
        ),
    ]
