# Generated by Django 4.1.4 on 2023-01-26 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend', '0013_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photo'),
        ),
    ]
