# Generated by Django 5.0.3 on 2024-03-20 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('owner', models.TextField()),
                ('where', models.TextField()),
                ('when', models.TextField()),
                ('Note', models.TextField()),
                ('current_user_number', models.IntegerField()),
                ('current_users', models.TextField()),
                ('max_user_num', models.IntegerField()),
            ],
        ),
    ]
