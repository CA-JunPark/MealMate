# Generated by Django 5.0.3 on 2024-03-23 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_account_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=models.ImageField(default='default_profile.png', upload_to='C:\\Users\\cskok\\Downloads\\My_Stuff\\CodingWorkSpcae\\PythonWorkSpace\\MealMate\\mealmate\\media'),
        ),
    ]