# Generated by Django 4.1.7 on 2023-06-11 16:06

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='media',
            field=models.ImageField(upload_to=posts.models.user_directory_path),
        ),
    ]
