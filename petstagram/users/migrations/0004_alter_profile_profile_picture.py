# Generated by Django 4.1.7 on 2023-06-11 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='/static/profile_pics/default.jpg', upload_to='static/profile_pics'),
        ),
    ]